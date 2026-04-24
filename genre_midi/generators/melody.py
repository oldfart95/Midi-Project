from __future__ import annotations

import random

from ..midi import NoteEvent
from ..theory import generate_scale, transpose_pitch_to_range


def generate_melody(arrangement: list[dict], recipe: dict, key: str, scale_name: str, bar_roots: list[int], seed: int) -> list[NoteEvent]:
    rng = random.Random(seed + 29)
    density_base = float(recipe["melody"].get("density", 0.4))
    contour = recipe["melody"].get("contour", "arch")
    scale = generate_scale(key, scale_name)
    events: list[NoteEvent] = []
    for bar in arrangement:
        idx = bar["bar_index"]
        bstart = idx * 4.0
        density = min(1.0, max(0.05, density_base + (bar["energy"] - 0.5) * 0.5))
        steps = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
        for s in steps:
            if rng.random() > density:
                continue
            chord_root = bar_roots[idx] % 12
            strong = s.is_integer()
            if strong and rng.random() < 0.7:
                pc = chord_root
            else:
                pc = rng.choice(scale)
            octave_bias = 72
            if contour == "rising":
                octave_bias += int((idx / max(1, len(arrangement)-1)) * 8)
            elif contour == "falling":
                octave_bias += int((1 - idx / max(1, len(arrangement)-1)) * 8)
            elif contour == "arch":
                center_dist = abs((idx / max(1, len(arrangement)-1)) - 0.5)
                octave_bias += int((0.5 - center_dist) * 10)
            pitch = transpose_pitch_to_range(octave_bias + pc - (octave_bias % 12), 60, 96)
            events.append(NoteEvent("lead", bstart + s, 0.45, pitch, 88, channel=3))
    return events
