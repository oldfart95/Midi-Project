from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict

import mido

TICKS_PER_BEAT = 480


@dataclass
class NoteEvent:
    track: str
    start: float
    duration: float
    pitch: int
    velocity: int
    channel: int = 0


def _beat_to_ticks(beat: float) -> int:
    return int(round(beat * TICKS_PER_BEAT))


def write_midi(
    output_path: str,
    events: list[NoteEvent],
    tempo_bpm: int,
    time_signature: str = "4/4",
    track_programs: dict[str, int] | None = None,
    include_tracks: list[str] | None = None,
) -> str:
    target_tracks = include_tracks or ["drums", "bass", "chords", "lead"]
    programs = track_programs or {}

    mid = mido.MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    meta_track = mido.MidiTrack()
    mid.tracks.append(meta_track)
    meta_track.append(mido.MetaMessage("track_name", name="meta", time=0))
    meta_track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo_bpm), time=0))
    nn, dd = time_signature.split("/")
    meta_track.append(mido.MetaMessage("time_signature", numerator=int(nn), denominator=int(dd), time=0))

    grouped: dict[str, list[tuple[int, mido.Message]]] = defaultdict(list)
    for ev in sorted(events, key=lambda e: (e.start, e.track, e.pitch, e.duration)):
        if ev.track not in target_tracks:
            continue
        start = max(0, _beat_to_ticks(ev.start))
        end = max(start + 1, _beat_to_ticks(ev.start + ev.duration))
        grouped[ev.track].append((start, mido.Message("note_on", note=ev.pitch, velocity=ev.velocity, channel=ev.channel, time=0)))
        grouped[ev.track].append((end, mido.Message("note_off", note=ev.pitch, velocity=0, channel=ev.channel, time=0)))

    for track_name in target_tracks:
        track = mido.MidiTrack()
        mid.tracks.append(track)
        track.append(mido.MetaMessage("track_name", name=track_name, time=0))
        channel = 9 if track_name == "drums" else {"bass": 1, "chords": 2, "lead": 3}.get(track_name, 0)
        if track_name != "drums":
            track.append(mido.Message("program_change", program=programs.get(track_name, 0), channel=channel, time=0))
        abs_events = sorted(grouped.get(track_name, []), key=lambda item: (item[0], 0 if item[1].type == "note_off" else 1, item[1].note))
        cursor = 0
        for tick, msg in abs_events:
            msg.time = tick - cursor
            cursor = tick
            track.append(msg)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    mid.save(out)
    return str(out)
