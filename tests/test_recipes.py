import pytest

from genre_midi.recipes import list_builtin_genres, load_recipe, RecipeValidationError, validate_recipe


def test_builtin_genres_complete():
    got = set(list_builtin_genres())
    assert {"synthwave", "edm", "trance", "chillwave", "gospel_ballad", "boom_bap", "ambient", "chiptune"}.issubset(got)


def test_builtin_loads_and_validates():
    for g in list_builtin_genres():
        recipe = load_recipe(genre=g)
        assert validate_recipe(recipe)["name"]


def test_bad_recipe_error():
    with pytest.raises(RecipeValidationError):
        validate_recipe({"name": "bad"})
