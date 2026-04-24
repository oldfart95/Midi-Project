from __future__ import annotations

from ..midi import NoteEvent

DRUMS = {"kick": 36, "snare": 38, "hat_closed": 42, "hat_open": 46, "clap": 39, "tom_low": 45, "tom_mid": 47, "crash": 49, "ride": 51}


def _add(events, bar_start, beat, pitch, vel):
    events.append(NoteEvent("drums", bar_start + beat, 0.1, pitch, vel, channel=9))


def generate_drums(arrangement: list[dict], recipe: dict) -> list[NoteEvent]:
    style = recipe["drums"].get("kick", "four_on_floor")
    hats = recipe["drums"].get("hats", "eighths")
    snare_style = recipe["drums"].get("snare", "backbeat")
    fills = bool(recipe["drums"].get("fills", False))
    events: list[NoteEvent] = []
    for i, bar in enumerate(arrangement):
        bar_start = bar["bar_index"] * 4.0
        e = bar["energy"]
        vel = int(65 + e * 35)
        if style in {"four_on_floor", "chiptune_simple"}:
            for b in [0, 1, 2, 3]:
                _add(events, bar_start, b, DRUMS["kick"], vel)
        elif style in {"boom_bap", "breakbeat_light"}:
            for b in [0, 2.5]:
                _add(events, bar_start, b, DRUMS["kick"], vel)
        elif style == "ambient_sparse":
            _add(events, bar_start, 0, DRUMS["kick"], vel - 10)

        if snare_style in {"backbeat", "boom_bap"}:
            for b in [1, 3]:
                _add(events, bar_start, b, DRUMS["snare"], vel - 5)
        elif snare_style == "half_time":
            _add(events, bar_start, 2, DRUMS["snare"], vel)

        if hats == "eighths":
            for k in range(8):
                _add(events, bar_start, k * 0.5, DRUMS["hat_closed"], vel - 20)
        elif hats == "quarters":
            for k in range(4):
                _add(events, bar_start, float(k), DRUMS["hat_closed"], vel - 18)

        if i == 0 and e >= 0.75:
            _add(events, bar_start, 0, DRUMS["crash"], vel + 5)
        if fills and i < len(arrangement) - 1 and arrangement[i + 1]["section"] != bar["section"]:
            _add(events, bar_start, 3.5, DRUMS["tom_low"], vel)
            _add(events, bar_start, 3.75, DRUMS["tom_mid"], vel)
    return events
