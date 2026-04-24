"""Lightweight local fallback for environments without external mido package."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


def bpm2tempo(bpm: int) -> int:
    return int(60_000_000 / bpm)


@dataclass
class Message:
    type: str
    time: int = 0
    note: int = 0
    velocity: int = 0
    channel: int = 0
    program: int = 0


@dataclass
class MetaMessage:
    type: str
    time: int = 0
    name: str = ""
    tempo: int = 500000
    numerator: int = 4
    denominator: int = 4


class MidiTrack(list):
    pass


class MidiFile:
    def __init__(self, filename: str | None = None, ticks_per_beat: int = 480):
        self.ticks_per_beat = ticks_per_beat
        self.tracks: list[MidiTrack] = []
        if filename:
            self._load(filename)

    def save(self, filename: str | Path):
        data = {
            "ticks_per_beat": self.ticks_per_beat,
            "tracks": [
                [vars(msg) | {"_cls": msg.__class__.__name__} for msg in track]
                for track in self.tracks
            ],
        }
        Path(filename).write_text(json.dumps(data))

    def _load(self, filename: str | Path):
        data = json.loads(Path(filename).read_text())
        self.ticks_per_beat = data["ticks_per_beat"]
        self.tracks = []
        for tr in data["tracks"]:
            track = MidiTrack()
            for item in tr:
                cls = item.pop("_cls")
                if cls == "MetaMessage":
                    track.append(MetaMessage(**item))
                else:
                    track.append(Message(**item))
            self.tracks.append(track)
