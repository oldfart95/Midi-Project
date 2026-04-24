from __future__ import annotations

import argparse
from dataclasses import asdict
import json

from .engine import GenerateOptions, generate_song
from .pack import generate_pack
from .preview import render_preview
from .progressions import render_progressions
from .recipes import list_builtin_genres


def _print_meta(meta):
    d = asdict(meta)
    for k, v in d.items():
        print(f"{k}: {v}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="genre-midi")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-genres")

    p_make = sub.add_parser("make")
    p_pack = sub.add_parser("pack")
    p_prog = sub.add_parser("progressions")
    p_prev = sub.add_parser("preview")

    for p in [p_make, p_pack, p_prog]:
        p.add_argument("--genre")
        p.add_argument("--recipe")
        p.add_argument("--key")
    for p in [p_make, p_pack]:
        p.add_argument("--tempo", type=int)
        p.add_argument("--bars", type=int)
        p.add_argument("--seed", type=int)
        p.add_argument("--randomize", action="store_true")
        p.add_argument("--stems", action="store_true")
    p_make.add_argument("--out", default="out/song.mid")

    p_pack.add_argument("--count", type=int, default=25)
    p_pack.add_argument("--out", default="packs/ideas")

    p_prog.add_argument("--limit", type=int, default=20)

    p_prev.add_argument("--midi", required=True)
    p_prev.add_argument("--soundfont", required=True)
    p_prev.add_argument("--out", required=True)

    args = parser.parse_args(argv)

    if args.cmd == "list-genres":
        for g in list_builtin_genres():
            print(g)
        return 0
    if args.cmd == "make":
        opts = GenerateOptions(args.genre, args.recipe, args.key, args.tempo, args.bars, args.seed, args.out, args.stems, args.randomize)
        meta = generate_song(opts)
        _print_meta(meta)
        return 0
    if args.cmd == "pack":
        opts = GenerateOptions(args.genre, args.recipe, args.key, args.tempo, args.bars, args.seed, output="", stems=args.stems, randomize=args.randomize)
        manifest = generate_pack(opts, args.count, args.out)
        print(json.dumps({"count": manifest["count"], "manifest": f"{args.out}/manifest.json"}, indent=2))
        return 0
    if args.cmd == "progressions":
        for line in render_progressions(args.genre, args.recipe, args.key or "C_major", args.limit):
            print(line)
        return 0
    if args.cmd == "preview":
        return render_preview(args.midi, args.soundfont, args.out)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
