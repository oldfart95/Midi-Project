from __future__ import annotations

import random

from .midi import NoteEvent


def humanize_events(
    events: list[NoteEvent],
    timing_ms: int,
    velocity_amount: int,
    note_length_amount: float,
    swing: float,
    seed: int,
    tempo: int,
) -> list[NoteEvent]:
    rng = random.Random(seed)
    beats_per_ms = tempo / 60000.0
    timing_beats = timing_ms * beats_per_ms
    out: list[NoteEvent] = []
    for ev in events:
        start = ev.start
        if swing and int(ev.start * 2) % 2 == 1:
            start += swing * 0.5
        start += rng.uniform(-timing_beats, timing_beats)
        start = max(0.0, start)
        dur = max(0.05, ev.duration + rng.uniform(-note_length_amount, note_length_amount))
        vel = max(1, min(127, ev.velocity + rng.randint(-velocity_amount, velocity_amount)))
        out.append(NoteEvent(track=ev.track, start=start, duration=dur, pitch=ev.pitch, velocity=vel, channel=ev.channel))
    return out
