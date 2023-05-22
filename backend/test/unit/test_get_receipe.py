import pytest
from unittest.mock import MagicMock

from src.controllers.receipecontroller import ReceipeController
from src.util.calculator import calculate_readiness
from src.static.diets import Diet

@pytest.fixture
def mocked_calculate_readiness():
    return MagicMock(side_effect=calculate_readiness)

@pytest.mark.unit
# A recipe containing required ingredients, a pantry with all ingredients available and a dietary restriction set to a valid value.
def test_all_valid(mocked_calculate_readiness):
    recipe = {'name': 'Recipe 1', 'diets': ['vegan'], 'ingredients': {'Egg': 5}}
    available_items = {'Egg': 10}

    mocked_calculate_readiness.return_value = 0.5

    readiness = ReceipeController.get_receipe_readiness(recipe, available_items, Diet.VEGAN)

    assert readiness == {'Recipe 1': 0.5}

@pytest.mark.unit
# A recipe containing required ingredients, a pantry with all ingredients available and a dietary restriction set to a value not supported by the recipe.
def test_not_matching_diet(mocked_calculate_readiness):
    recipe = {'name': 'Recipe 2', 'diets': ['normal'], 'ingredients': {'Egg': 5}}
    available_items = {'Egg': 10}

    mocked_calculate_readiness.return_value = 0.05

    readiness = ReceipeController.get_receipe_readiness(recipe, available_items, Diet.VEGAN)

    assert readiness is None

# A recipe containing required ingredients, a pantry with a subset of ingredients available and a dietary restriction set to a valid value.

@pytest.mark.unit
# A recipe containing required ingredients and a pantry with none of the ingredients available and a dietary restriction set to a valid value.
def test_unfulfilled_pantry():
    recipe = {'name': 'Recipe 4', 'diets': ['vegetarian'], 'ingredients': {'Egg': 5}}
    available_items = {}

    readiness = ReceipeController.get_receipe_readiness(recipe, available_items, Diet.VEGETARIAN)

    assert readiness is None


