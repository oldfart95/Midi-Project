# genre-midi-lab

Generate original MIDI ideas from editable YAML genre recipes.

## Install

```bash
python -m pip install -e ".[dev]"
```

## Basic usage

```bash
genre-midi list-genres
genre-midi make --genre synthwave --out out/demo.mid
```

## Pack mode

```bash
genre-midi pack --genre synthwave --count 25 --bars 16 --out packs/synthwave
```

## Stem export

```bash
genre-midi make --genre boom_bap --stems --out out/beat.mid
```

## Progression browser

```bash
genre-midi progressions --genre gospel_ballad --key C_major
```

## Preview helper (optional)

```bash
genre-midi preview --midi out/demo.mid --soundfont path/to/font.sf2 --out out/demo.wav
```

FluidSynth is optional and not a required dependency.

## Python API

```python
from genre_midi.engine import GenerateOptions, generate_song
meta = generate_song(GenerateOptions(genre="synthwave", output="out/demo.mid", seed=123))
print(meta)
```

## Custom recipe format

Use keys: `name`, `tempo`, `default_key`, `scale_pool`, `sections`, `chords`, `bass`, `drums`, `melody`, `tracks`.
See `genre_midi/presets/*.yaml` for complete examples.

## Built-in genres

- synthwave
- edm
- trance
- chillwave
- gospel_ballad
- boom_bap
- ambient
- chiptune

## Copyright boundary

This library generates original MIDI from broad genre recipes. It does not copy songs or artist-specific melodies.

## Troubleshooting

- If `genre-midi` command is missing, reinstall editable package.
- If preview fails, install FluidSynth and verify `fluidsynth` is on PATH.
- If YAML fails to load, check required recipe keys.

## Suggested workflows

- DAW import and arrangement extension.
- Koala Sampler chop and resample workflow.
- Android music app import for sketching.
- Pack generation for composition starting points.
