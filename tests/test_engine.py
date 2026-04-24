from genre_midi.engine import GenerateOptions, generate_song


def test_generate_song_creates_midi(tmp_path):
    out = tmp_path / "song.mid"
    meta = generate_song(GenerateOptions(genre="synthwave", output=str(out), seed=1))
    assert out.exists()
    assert meta.seed == 1


def test_seed_metadata_consistency(tmp_path):
    out1 = tmp_path / "a.mid"
    out2 = tmp_path / "b.mid"
    m1 = generate_song(GenerateOptions(genre="synthwave", output=str(out1), seed=44))
    m2 = generate_song(GenerateOptions(genre="synthwave", output=str(out2), seed=44))
    assert m1.selected_progression == m2.selected_progression


def test_randomize_deterministic_with_seed(tmp_path):
    a = generate_song(GenerateOptions(genre="chillwave", output=str(tmp_path / "c.mid"), seed=99, randomize=True))
    b = generate_song(GenerateOptions(genre="chillwave", output=str(tmp_path / "d.mid"), seed=99, randomize=True))
    assert (a.key, a.tempo, a.selected_progression) == (b.key, b.tempo, b.selected_progression)


def test_bars_override(tmp_path):
    m = generate_song(GenerateOptions(genre="ambient", bars=10, output=str(tmp_path / "e.mid"), seed=2))
    assert m.bars == 10
