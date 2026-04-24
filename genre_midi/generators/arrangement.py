from __future__ import annotations


def build_arrangement(sections: list[dict], bars_override: int | None = None) -> list[dict]:
    expanded: list[dict] = []
    for sec in sections:
        for _ in range(int(sec["bars"])):
            expanded.append({"section": sec["name"], "energy": float(sec.get("energy", 0.5))})
    if bars_override is None:
        target = len(expanded)
    else:
        target = bars_override
    if not expanded:
        return []
    arr = [expanded[i % len(expanded)] for i in range(target)]
    for i, bar in enumerate(arr):
        bar["bar_index"] = i
    return arr
