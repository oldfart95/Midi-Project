from genre_midi.theory import (
    note_name_to_midi,
    midi_to_note_name,
    parse_key,
    generate_scale,
    build_chord_pitches,
    transpose_pitch_to_range,
)


def test_note_name_conversion():
    assert note_name_to_midi("C", 4) == 60
    assert midi_to_note_name(60) == "C4"


def test_key_parsing_and_scale():
    p = parse_key("A_minor")
    assert p.tonic == "A"
    s = generate_scale("C_major", "major")
    assert s[0] == 0 and len(s) == 7


def test_roman_chord_generation():
    chord = build_chord_pitches("C_major", "major", "Imaj7")
    assert len(chord) == 4


def test_pitch_range_utility():
    assert 36 <= transpose_pitch_to_range(24, 36, 60) <= 60
