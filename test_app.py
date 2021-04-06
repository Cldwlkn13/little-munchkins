from app_definitions import AppDefinitions
from app import app
import unittest

app.testing = True
defs = AppDefinitions()


class TestApp(unittest.TestCase):
    # Testing isFavourited()
    def test_isFavourited_emptyFavouritesWithNoId_expectFalse(self):
        user = {'favourites': []}
        _id = ""
        isfav = defs.isFavourited(user, _id)
        self.assertFalse(isfav)

    def test_isFavourited_hasFavouritesWithCorrectId_expectTrue(self):
        user = {'favourites': ["thisshouldpass"]}
        _id = "thisshouldpass"
        isfav = defs.isFavourited(user, _id)
        self.assertTrue(isfav)

    def test_isFavourited_hasFavouritesWithIncCorrectId_expectFalse(self):
        user = {'favourites': ["Iwanttopass"]}
        _id = "thisshouldnotpass"
        isfav = defs.isFavourited(user, _id)
        self.assertFalse(isfav)

    def test_isFavourited_hasNoFavourites_expectFalse(self):
        user = {}
        _id = "thisshouldnotpass"
        isfav = defs.isFavourited(user, _id)
        self.assertFalse(isfav)

    def test_isFavourited_hasNoId_expectFalse(self):
        user = {'favourites': ["Iwanttopass"]}
        _id = ""
        isfav = defs.isFavourited(user, _id)
        self.assertFalse(isfav)

    # Testing recipeCardBuilder() (rcb) ---> groupFormKeys() ---> stepsBuilder()/ingredientsBuilder()
    def test_rcb_withSimpleObj_shouldReturnRecipeCard(self):
        requestform = {
            "title": "test",
            "desc": "test desc",
            "recipe_img_name": "test_img",
            "portions": 4,
            "min": 1,
            "max": 72,
        }
        recipeCard = defs.recipeCardBuilder(requestform, "")
        self.assertIsNotNone(recipeCard)
        self.assertEqual(recipeCard['title'], "test")
        self.assertEqual(recipeCard['portions'], 4)
        self.assertEqual(recipeCard['suitableForMinMnths'], 1)

    def test_rcb_withOneIngredientAndOneStep_shouldReturnRecipeCard(self):
        requestform = {
            "title": "test",
            "desc": "test desc",
            "recipe_img_name": "test_img.jpg",
            "portions": 4,
            "min": 1,
            "max": 72,
            "ingredient-1-desc": "test_ingredient",
            "ingredient-1-measure": 100,
            "ingredient-1-unit": "g",
            "step-1-desc": "test_step",
            "step-1-type": "prepare",
            "step-1-time": 5,
        }
        recipeCard = defs.recipeCardBuilder(requestform, "")
        self.assertIsNotNone(recipeCard)
        self.assertEqual(recipeCard['recipe_img'], "test_img.jpg")
        self.assertEqual(recipeCard['suitableForMaxMnths'], 72)
        self.assertIsNotNone(recipeCard['ingredients']['0'])
        self.assertEqual(
            recipeCard['ingredients']['0']['name'], "test_ingredient")

    def test_rcb_withManyIngredientsAndManySteps_shouldReturnRecipeCard(self):
        requestform = {
            "title": "test",
            "desc": "test desc",
            "recipe_img_name": "test_img.jpg",
            "portions": 4,
            "min": 1,
            "max": 72,
            "ingredient-1-desc": "test_ingredient",
            "ingredient-1-measure": 100,
            "ingredient-1-unit": "g",
            "ingredient-2-desc": "test_ingredient_2",
            "ingredient-2-measure": 100,
            "ingredient-2-unit": "g",
            "step-1-desc": "test_step",
            "step-1-type": "prepare",
            "step-1-time": 5,
            "step-2-desc": "test_step_2",
            "step-2-type": "prepare",
            "step-2-time": 5,
        }
        recipeCard = defs.recipeCardBuilder(requestform, "")
        self.assertIsNotNone(recipeCard['ingredients']['0'])
        self.assertIsNotNone(recipeCard['ingredients']['1'])
        self.assertEqual(
            recipeCard['ingredients']['0']['name'], "test_ingredient")
        self.assertEqual(
            recipeCard['ingredients']['1']['name'], "test_ingredient_2")
        self.assertEqual(
            recipeCard['steps']['0']['action'], "test_step")
        self.assertEqual(
            recipeCard['steps']['1']['action'], "test_step_2")

    def test_rcb_withIngredAndStepsWrongOrder_shouldReturnRecipeCard(self):
        requestform = {
            "title": "test",
            "desc": "test desc",
            "recipe_img_name": "test_img.jpg",
            "portions": 4,
            "min": 1,
            "max": 72,
            "ingredient-2-desc": "test_ingredient_2",
            "ingredient-2-measure": 100,
            "ingredient-2-unit": "g",
            "step-2-desc": "test_step_2",
            "step-2-type": "prepare",
            "step-2-time": 5,
        }
        recipeCard = defs.recipeCardBuilder(requestform, "test_user")
        self.assertEqual(recipeCard['created_by'], "test_user")
        self.assertIsNotNone(recipeCard['ingredients']['0'])
        self.assertEqual(
            recipeCard['ingredients']['0']['name'], "test_ingredient_2")
        self.assertEqual(
            recipeCard['steps']['0']['action'], "test_step_2")

    # Testing calculateTiming()
    def test_calculateTiming_WithOneStep_AssertTrue(self):
        requestform = {
            "title": "test",
            "desc": "test desc",
            "recipe_img_name": "test_img.jpg",
            "portions": 4,
            "min": 1,
            "max": 72,
            "step-1-desc": "test_step",
            "step-1-type": "prepare",
            "step-1-time": 5,
        }
        recipeCard = defs.recipeCardBuilder(requestform, "test_user")
        t = defs.calculateTiming(recipeCard, "prepare")
        self.assertEqual(t, 5)

    def test_calculateTiming_WithManySteps_AssertTrue(self):
        requestform = {
            "title": "test",
            "desc": "test desc",
            "recipe_img_name": "test_img.jpg",
            "portions": 4,
            "min": 1,
            "max": 72,
            "step-1-desc": "test_step",
            "step-1-type": "prepare",
            "step-1-time": 5,
            "step-2-desc": "test_step_2",
            "step-2-type": "prepare",
            "step-2-time": 5,
            "step-3-desc": "test_step_3",
            "step-3-type": "prepare",
            "step-3-time": 7,
        }
        recipeCard = defs.recipeCardBuilder(requestform, "test_user")
        t = defs.calculateTiming(recipeCard, "prepare")
        self.assertEqual(t, 17)

    # Testing http endpoints
    def test_callHome(self):
        self.app = app.test_client()
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

