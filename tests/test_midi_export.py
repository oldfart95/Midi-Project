import mido

from genre_midi.engine import GenerateOptions, generate_song


def test_full_export_non_empty(tmp_path):
    p = tmp_path / "full.mid"
    generate_song(GenerateOptions(genre="synthwave", output=str(p), seed=3))
    assert p.exists() and p.stat().st_size > 0
    mido.MidiFile(str(p))


def test_stem_export(tmp_path):
    p = tmp_path / "full.mid"
    meta = generate_song(GenerateOptions(genre="boom_bap", output=str(p), stems=True, seed=4))
    assert meta.stem_paths
    for fp in meta.stem_paths.values():
        assert mido.MidiFile(fp)
