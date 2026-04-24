from genre_midi.engine import GenerateOptions
from genre_midi.pack import generate_pack

manifest = generate_pack(GenerateOptions(genre="synthwave", bars=16, seed=1000), count=5, out_dir="packs/example_pack")
print(manifest["count"])
