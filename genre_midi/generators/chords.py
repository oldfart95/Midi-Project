from __future__ import annotations

import random

from ..midi import NoteEvent
from ..theory import build_chord_pitches, transpose_pitch_to_range


def generate_chords(arrangement: list[dict], recipe: dict, key: str, scale: str, seed: int) -> tuple[list[NoteEvent], list[str], list[int]]:
    rng = random.Random(seed + 11)
    progression = rng.choice(recipe["chords"]["progression_pool"])
    rhythm = recipe["chords"].get("rhythm", "whole_notes")
    events: list[NoteEvent] = []
    bar_roots: list[int] = []
    for bar in arrangement:
        bar_start = bar["bar_index"] * 4.0
        roman = progression[bar["bar_index"] % len(progression)]
        chord = [transpose_pitch_to_range(n, 48, 84) for n in build_chord_pitches(key, scale, roman, octave=4)]
        bar_roots.append(chord[0])
        starts = [0.0]
        duration = 4.0
        if rhythm == "half_notes":
            starts, duration = [0.0, 2.0], 2.0
        elif rhythm == "quarter_pulse":
            starts, duration = [0.0, 1.0, 2.0, 3.0], 1.0
        elif rhythm == "syncopated":
            starts, duration = [0.0, 1.5, 3.0], 1.0
        elif rhythm == "stabs":
            starts, duration = [0.0, 2.0, 3.5], 0.4
        for s in starts:
            for p in chord:
                events.append(NoteEvent("chords", bar_start + s, duration, p, 68, channel=2))
    return events, progression, bar_roots
