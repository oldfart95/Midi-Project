from genre_midi.engine import GenerateOptions, generate_song

meta = generate_song(GenerateOptions(genre="chiptune", tempo=140, output="out/example_chiptune.mid", seed=123))
print(meta)
