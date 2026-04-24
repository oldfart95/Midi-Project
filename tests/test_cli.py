from genre_midi.cli import main


def test_list_genres(capsys):
    rc = main(["list-genres"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "synthwave" in out


def test_make_output(tmp_path):
    rc = main(["make", "--genre", "synthwave", "--seed", "8", "--out", str(tmp_path / "x.mid")])
    assert rc == 0
    assert (tmp_path / "x.mid").exists()


def test_make_stems(tmp_path):
    full = tmp_path / "y.mid"
    rc = main(["make", "--genre", "boom_bap", "--stems", "--seed", "9", "--out", str(full)])
    assert rc == 0
    assert (tmp_path / "y_drums.mid").exists()


def test_make_randomize(tmp_path):
    rc = main(["make", "--genre", "chillwave", "--randomize", "--seed", "10", "--out", str(tmp_path / "z.mid")])
    assert rc == 0
