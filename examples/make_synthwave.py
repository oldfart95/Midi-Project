from genre_midi.engine import GenerateOptions, generate_song

meta = generate_song(GenerateOptions(genre="synthwave", output="out/example_synthwave.mid", seed=42))
print(meta)
