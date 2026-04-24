from __future__ import annotations

from ..midi import NoteEvent
from ..theory import transpose_pitch_to_range


def generate_bass(arrangement: list[dict], bar_roots: list[int], recipe: dict) -> list[NoteEvent]:
    style = recipe["bass"].get("style", "root_notes")
    base_density = float(recipe["bass"].get("density", 0.6))
    events: list[NoteEvent] = []
    for bar in arrangement:
        idx = bar["bar_index"]
        start = idx * 4.0
        root = transpose_pitch_to_range(bar_roots[idx] - 24, 36, 60)
        density = min(1.0, base_density + (bar["energy"] - 0.5) * 0.4)
        pattern = [(0.0, 1.0), (2.0, 1.0)]
        if style in {"octave_pulse", "arpeggiated", "chiptune_square"}:
            pattern = [(0.0, 0.5), (0.5, 0.5), (1.0, 0.5), (1.5, 0.5), (2.0, 0.5), (2.5, 0.5), (3.0, 0.5), (3.5, 0.5)]
        elif style == "offbeat":
            pattern = [(0.5, 0.5), (1.5, 0.5), (2.5, 0.5), (3.5, 0.5)]
        elif style == "walking":
            pattern = [(i * 1.0, 1.0) for i in range(4)]
        for s, d in pattern:
            if density < 0.5 and s % 2 != 0:
                continue
            pitch = root
            if style in {"octave_pulse", "arpeggiated", "chiptune_square"} and int(s * 2) % 2 == 1:
                pitch = transpose_pitch_to_range(root + 12, 36, 60)
            if style == "walking" and s in {1.0, 3.0}:
                pitch = transpose_pitch_to_range(root + 2, 36, 60)
            dur = 0.22 if style == "chiptune_square" else d
            events.append(NoteEvent("bass", start + s, dur, pitch, 82, channel=1))
    return events
