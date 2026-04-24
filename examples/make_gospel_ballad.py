from genre_midi.engine import GenerateOptions, generate_song

meta = generate_song(GenerateOptions(genre="gospel_ballad", key="C_major", tempo=72, output="out/example_gospel.mid", seed=77))
print(meta)
