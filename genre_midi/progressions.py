from __future__ import annotations

from .recipes import load_recipe
from .theory import build_chord_pitches, midi_to_note_name


def render_progressions(genre: str | None, recipe_path: str | None, key: str, limit: int = 20) -> list[str]:
    recipe = load_recipe(genre, recipe_path)
    scale = recipe["scale_pool"][0]
    lines = []
    for i, prog in enumerate(recipe["chords"]["progression_pool"][:limit], start=1):
        chords = []
        for roman in prog:
            notes = [midi_to_note_name(n)[:-1] for n in build_chord_pitches(key, scale, roman, octave=4)[:3]]
            chords.append(f"{roman} ({'-'.join(notes)})")
        lines.append(f"{i:02d}. {' | '.join(chords)}")
    return lines
