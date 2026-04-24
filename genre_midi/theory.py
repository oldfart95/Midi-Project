from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable

NOTE_TO_SEMITONE = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}
SEMITONE_TO_NOTE = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

SCALE_INTERVALS = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "natural_minor": [0, 2, 3, 5, 7, 8, 10],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "melodic_minor": [0, 2, 3, 5, 7, 9, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "pentatonic_major": [0, 2, 4, 7, 9],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "blues_minor": [0, 3, 5, 6, 7, 10],
    "minor": [0, 2, 3, 5, 7, 8, 10],
}

ROMAN_TO_DEGREE = {
    "I": 1, "ii": 2, "iii": 3, "IV": 4, "V": 5, "vi": 6, "vii°": 7,
    "i": 1, "ii°": 2, "III": 3, "iv": 4, "v": 5, "VI": 6, "VII": 7,
}


@dataclass(frozen=True)
class ParsedKey:
    tonic: str
    mode: str


def note_name_to_midi(note: str, octave: int = 4) -> int:
    if note not in NOTE_TO_SEMITONE:
        raise ValueError(f"Unknown note name: {note}")
    return 12 * (octave + 1) + NOTE_TO_SEMITONE[note]


def midi_to_note_name(pitch: int) -> str:
    note = SEMITONE_TO_NOTE[pitch % 12]
    octave = pitch // 12 - 1
    return f"{note}{octave}"


def parse_key(key: str) -> ParsedKey:
    try:
        tonic, mode = key.split("_", 1)
    except ValueError as exc:
        raise ValueError(f"Invalid key format '{key}'. Use like C_major or A_minor") from exc
    if tonic not in NOTE_TO_SEMITONE:
        raise ValueError(f"Unknown tonic in key '{key}'")
    if mode not in {"major", "minor"}:
        raise ValueError(f"Unsupported key mode '{mode}'. Use major/minor")
    return ParsedKey(tonic=tonic, mode=mode)


def generate_scale(key: str, scale_name: str | None = None) -> list[int]:
    parsed = parse_key(key)
    chosen = scale_name or ("major" if parsed.mode == "major" else "natural_minor")
    if chosen not in SCALE_INTERVALS:
        raise ValueError(f"Unsupported scale '{chosen}'")
    root = NOTE_TO_SEMITONE[parsed.tonic]
    return [(root + i) % 12 for i in SCALE_INTERVALS[chosen]]


def roman_to_degree(roman: str) -> tuple[int, bool]:
    clean = roman.replace("7", "").replace("maj", "")
    if clean not in ROMAN_TO_DEGREE:
        raise ValueError(f"Unknown Roman numeral '{roman}' in progression")
    return ROMAN_TO_DEGREE[clean], "7" in roman


def build_chord_pitches(key: str, scale_name: str, roman: str, octave: int = 4) -> list[int]:
    degree, seventh = roman_to_degree(roman)
    scale = generate_scale(key, scale_name)
    root_pc = scale[(degree - 1) % len(scale)]
    third_pc = scale[(degree + 1) % len(scale)]
    fifth_pc = scale[(degree + 3) % len(scale)]
    pcs = [root_pc, third_pc, fifth_pc]
    if seventh:
        pcs.append(scale[(degree + 5) % len(scale)])
    base = 12 * (octave + 1)
    notes: list[int] = []
    for pc in pcs:
        pitch = base + pc
        while notes and pitch <= notes[-1]:
            pitch += 12
        notes.append(pitch)
    return notes


def clamp_midi_note(pitch: int, low: int = 0, high: int = 127) -> int:
    return max(low, min(high, pitch))


def choose_from_weighted_pool(pool: Iterable[tuple[object, float]], rng: random.Random):
    vals, weights = zip(*pool)
    return rng.choices(vals, weights=weights, k=1)[0]


def quantize_beat(beat: float, resolution: float = 0.25) -> float:
    return round(beat / resolution) * resolution


def bars_to_beats(bars: int, beats_per_bar: int = 4) -> int:
    return bars * beats_per_bar


def transpose_pitch_to_range(pitch: int, low: int, high: int) -> int:
    while pitch < low:
        pitch += 12
    while pitch > high:
        pitch -= 12
    return clamp_midi_note(pitch, low, high)
