from __future__ import annotations

from pathlib import Path
from importlib import resources
from typing import Any

import yaml

REQUIRED_FIELDS = [
    "name", "tempo", "default_key", "scale_pool", "sections", "chords", "bass", "drums", "melody", "tracks"
]


class RecipeValidationError(ValueError):
    pass


def list_builtin_genres() -> list[str]:
    base = resources.files("genre_midi").joinpath("presets")
    return sorted([p.name.replace(".yaml", "") for p in base.iterdir() if p.name.endswith(".yaml")])


def validate_recipe(recipe: dict[str, Any]) -> dict[str, Any]:
    missing = [f for f in REQUIRED_FIELDS if f not in recipe]
    if missing:
        raise RecipeValidationError(f"Recipe missing required fields: {', '.join(missing)}")
    if not isinstance(recipe.get("sections"), list) or not recipe["sections"]:
        raise RecipeValidationError("Recipe sections must be a non-empty list")
    if "progression_pool" not in recipe["chords"]:
        raise RecipeValidationError("Recipe chords.progression_pool is required")
    return recipe


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        raise RecipeValidationError(f"Failed to parse YAML: {path}") from exc
    if not isinstance(data, dict):
        raise RecipeValidationError("Recipe root must be a mapping")
    return validate_recipe(data)


def load_recipe(genre: str | None = None, recipe_path: str | None = None) -> dict[str, Any]:
    if not genre and not recipe_path:
        raise RecipeValidationError("Provide --genre or --recipe")
    if recipe_path:
        return _load_yaml(Path(recipe_path))
    preset_path = resources.files("genre_midi").joinpath("presets", f"{genre}.yaml")
    if not preset_path.is_file():
        raise RecipeValidationError(f"Unknown built-in genre '{genre}'. Use list-genres.")
    with resources.as_file(preset_path) as p:
        return _load_yaml(p)
