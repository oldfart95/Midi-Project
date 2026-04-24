from __future__ import annotations

import shutil
import subprocess


def render_preview(midi_path: str, soundfont: str, out_wav: str) -> int:
    if shutil.which("fluidsynth") is None:
        print("FluidSynth is not installed. Install it first, then retry preview.")
        return 1
    cmd = ["fluidsynth", "-ni", soundfont, midi_path, "-F", out_wav, "-r", "44100"]
    result = subprocess.run(cmd, check=False)
    return result.returncode
