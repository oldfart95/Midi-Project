from genre_midi.progressions import render_progressions


def test_progressions_synthwave_and_gospel():
    a = render_progressions("synthwave", None, "A_minor", limit=5)
    b = render_progressions("gospel_ballad", None, "C_major", limit=5)
    assert a and b
    assert "01." in a[0]
