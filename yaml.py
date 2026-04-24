"""Small fallback shim for yaml.safe_load using JSON-compatible YAML files."""
from __future__ import annotations

import json


class YAMLError(ValueError):
    pass


def safe_load(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise YAMLError(str(exc)) from exc
