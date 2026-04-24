from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from .engine import GenerateOptions, generate_song


def generate_pack(options: GenerateOptions, count: int, out_dir: str) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    items = []
    base_seed = options.seed if options.seed is not None else 1000
    prefix = options.genre or "custom"
    for i in range(count):
        idx = i + 1
        seed = base_seed + i
        if options.stems:
            output_name = f"{prefix}_{idx:03d}_full.mid"
        else:
            output_name = f"{prefix}_{idx:03d}.mid"
        item_opts = GenerateOptions(
            genre=options.genre,
            recipe_path=options.recipe_path,
            key=options.key,
            tempo=options.tempo,
            bars=options.bars,
            seed=seed,
            output=str(out / output_name),
            stems=options.stems,
            randomize=options.randomize,
        )
        meta = generate_song(item_opts)
        items.append(asdict(meta))

    manifest = {"count": count, "items": items}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest
