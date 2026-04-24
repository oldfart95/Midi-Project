from __future__ import annotations

from dataclasses import dataclass, asdict
import random
from pathlib import Path

from .generators.arrangement import build_arrangement
from .generators.chords import generate_chords
from .generators.bass import generate_bass
from .generators.drums import generate_drums
from .generators.melody import generate_melody
from .humanize import humanize_events
from .midi import NoteEvent, write_midi
from .recipes import load_recipe


@dataclass
class GenerateOptions:
    genre: str | None = None
    recipe_path: str | None = None
    key: str | None = None
    tempo: int | None = None
    bars: int | None = None
    seed: int | None = None
    output: str = "out/song.mid"
    stems: bool = False
    randomize: bool = False


@dataclass
class SongMetadata:
    output_path: str
    genre: str
    key: str
    tempo: int
    bars: int
    seed: int
    selected_progression: list[str]
    stem_paths: dict[str, str] | None = None


def _pick_key(rng: random.Random, prefer_minor: bool, prefer_major: bool) -> str:
    majors = ["C_major", "G_major", "D_major", "A_major", "F_major", "Bb_major"]
    minors = ["A_minor", "E_minor", "B_minor", "D_minor", "G_minor", "C_minor"]
    pool = majors + minors
    if prefer_minor:
        pool = minors + minors + majors
    if prefer_major:
        pool = majors + majors + minors
    return rng.choice(pool)


def generate_song(options: GenerateOptions) -> SongMetadata:
    recipe = load_recipe(options.genre, options.recipe_path)
    genre = options.genre or recipe.get("name", "custom")
    seed = options.seed if options.seed is not None else random.randint(1, 10_000_000)
    rng = random.Random(seed)

    tempo_min = int(recipe["tempo"]["min"])
    tempo_max = int(recipe["tempo"]["max"])
    tempo = options.tempo if options.tempo else rng.randint(tempo_min, tempo_max)

    prefer_minor = all("minor" in s for s in recipe.get("scale_pool", []) if isinstance(s, str))
    prefer_major = genre == "gospel_ballad"
    key = options.key or recipe.get("default_key", "C_major")
    if options.randomize and not options.key:
        key = _pick_key(rng, prefer_minor=prefer_minor, prefer_major=prefer_major)

    scale = rng.choice(recipe["scale_pool"]) if options.randomize else recipe["scale_pool"][0]
    arrangement = build_arrangement(recipe["sections"], options.bars)
    bars = len(arrangement)

    chord_events, progression, bar_roots = generate_chords(arrangement, recipe, key, scale, seed)
    bass_events = generate_bass(arrangement, bar_roots, recipe)
    drum_events = generate_drums(arrangement, recipe)
    melody_events = generate_melody(arrangement, recipe, key, scale, bar_roots, seed)
    all_events: list[NoteEvent] = chord_events + bass_events + drum_events + melody_events

    h = recipe.get("humanize", {})
    timing = int(h.get("timing_ms", 6))
    vel = int(h.get("velocity", 6))
    note_len = float(h.get("note_length", 0.05))
    swing = float(recipe.get("swing", 0.0))
    if options.randomize:
        timing = max(0, timing + rng.randint(-2, 2))
        vel = max(0, vel + rng.randint(-2, 2))
    humanized = humanize_events(all_events, timing, vel, note_len, swing, seed, tempo)

    programs = {
        "bass": int(recipe["tracks"].get("bass", {}).get("program", 38)),
        "chords": int(recipe["tracks"].get("chords", {}).get("program", 89)),
        "lead": int(recipe["tracks"].get("lead", {}).get("program", 81)),
    }
    out = write_midi(options.output, humanized, tempo, recipe.get("time_signature", "4/4"), programs)

    stem_paths = None
    if options.stems:
        stem_paths = {}
        base = Path(options.output)
        for track in ["drums", "bass", "chords", "lead"]:
            stem = str(base.with_name(f"{base.stem}_{track}.mid"))
            write_midi(stem, humanized, tempo, recipe.get("time_signature", "4/4"), programs, include_tracks=[track])
            stem_paths[track] = stem

    return SongMetadata(
        output_path=out,
        genre=genre,
        key=key,
        tempo=tempo,
        bars=bars,
        seed=seed,
        selected_progression=progression,
        stem_paths=stem_paths,
    )
