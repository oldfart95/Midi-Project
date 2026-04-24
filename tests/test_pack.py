import json

from genre_midi.engine import GenerateOptions
from genre_midi.pack import generate_pack


def test_pack_count_and_manifest(tmp_path):
    out = tmp_path / "pack"
    manifest = generate_pack(GenerateOptions(genre="synthwave", bars=8, seed=100), 3, str(out))
    assert manifest["count"] == 3
    data = json.loads((out / "manifest.json").read_text())
    assert len(data["items"]) == 3


def test_pack_stems(tmp_path):
    out = tmp_path / "pack2"
    generate_pack(GenerateOptions(genre="boom_bap", bars=8, seed=200, stems=True), 2, str(out))
    assert (out / "boom_bap_001_full.mid").exists()
    assert (out / "manifest.json").exists()


def test_pack_seed_deterministic(tmp_path):
    o1 = tmp_path / "p1"
    o2 = tmp_path / "p2"
    m1 = generate_pack(GenerateOptions(genre="synthwave", seed=300), 2, str(o1))
    m2 = generate_pack(GenerateOptions(genre="synthwave", seed=300), 2, str(o2))
    assert m1["items"][0]["selected_progression"] == m2["items"][0]["selected_progression"]
