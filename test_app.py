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

    def test_isFavourited_hasFavouritesWithIncorrectId_expectFalse(self):
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

    # Testing recipeCardBuilder() (rcb) ---> groupFormKeys() --->
    # stepsBuilder()/ingredientsBuilder()
    def test_rcb_withSimpleObj_expectRecipeCard(self):
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

    def test_rcb_withOneIngredientAndOneStep_expectRecipeCard(self):
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

    def test_rcb_withManyIngredientsAndManySteps_expectRecipeCard(self):
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

    def test_rcb_withIngredAndStepsWrongOrder_expectRecipeCard(self):
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

    # Testing groupFormKeys()
    def test_groupFormKeys_withOneSet_expectList(self):
        _keys = ['step-1-desc', 'step-1-type', 'step-1-time']
        _list = defs.groupFormKeys(_keys)
        self.assertIsNotNone(_list)
        self.assertTrue(len(_list), 1)
        self.assertEqual(
            str(_list[0]), "['step-1-desc', 'step-1-type', 'step-1-time']")

    def test_groupFormKeys_withManySets_expectList(self):
        _keys = [
            'step-1-desc',
            'step-1-type',
            'step-1-time',
            'step-2-desc',
            'step-2-type',
            'step-2-time'
        ]
        _list = defs.groupFormKeys(_keys)
        self.assertIsNotNone(_list)
        self.assertTrue(len(_list), 2)
        self.assertEqual(
            str(_list[1]), "['step-2-desc', 'step-2-type', 'step-2-time']")

    def test_groupFormKeys_withEmptyKeys_expectList(self):
        _keys = []
        _list = defs.groupFormKeys(_keys)
        self.assertEqual([], _list)

    # Testing stepsBuilder()
    def test_stepsBuilder_withKeysAndForm_expectObj(self):
        _groupedKeys = [['step-1-desc', 'step-1-type', 'step-1-time']]
        _requestform = {
            'step-1-desc': "test_desc",
            'step-1-type': "prepare",
            'step-1-time': 1
        }
        _steps = defs.stepsBuilder(_groupedKeys, _requestform)
        self.assertIsNotNone(_steps)
        self.assertEqual(_steps, {
            '0': {
                'type': 'prepare',
                'action': 'test_desc',
                'time': 1
            }
        })

    def test_stepsBuilder_withKeysAndNoForm_expectEmptyObj(self):
        _groupedKeys = [['step-1-desc', 'step-1-type', 'step-1-time']]
        _requestform = {}
        _steps = defs.stepsBuilder(_groupedKeys, _requestform)
        self.assertIsNotNone(_steps)
        self.assertEqual(_steps, {})

    def test_stepsBuilder_withNoKeysAndForm_expectEmptyObj(self):
        _groupedKeys = []
        _requestform = {
            'step-1-desc': "test_desc",
            'step-1-type': "prepare",
            'step-1-time': 1
        }
        _steps = defs.stepsBuilder(_groupedKeys, _requestform)
        self.assertIsNotNone(_steps)
        self.assertEqual(_steps, {})

    # Testing ingredientsBuilder()
    def test_ingredientsBuilder_withKeysAndForm_expectObj(self):
        _groupedKeys = [
            [
                'ingredient-1-desc',
                'ingredient-1-measure',
                'ingredient-1-unit'
            ]
        ]
        _requestform = {
             'ingredient-1-desc': "test_desc",
             'ingredient-1-measure': 100,
             'ingredient-1-unit': "g"
             }
        _ingredients = defs.ingredientsBuilder(_groupedKeys, _requestform)
        self.assertIsNotNone(_ingredients)
        self.assertEqual(_ingredients, {
            '0': {
                'name': 'test_desc',
                'qty': {
                    'measure': 100,
                    'unit': 'g'
                }
            }
        })

    def test_ingredientsBuilder_withKeysAndNoForm_expectEmptyObj(self):
        _groupedKeys = [
            [
                'ingredient-1-desc',
                'ingredient-1-measure',
                'ingredient-1-unit'
            ]
        ]
        _requestform = {}
        _ingredients = defs.ingredientsBuilder(_groupedKeys, _requestform)
        self.assertIsNotNone(_ingredients)
        self.assertEqual(_ingredients, {})

    def test_ingredientsBuilder_withNoKeysAndForm_expectEmptyObj(self):
        _groupedKeys = []
        _requestform = {
            'ingredient-1-desc': "test_desc",
            'ingredient-1-measure': 100,
            'ingredient-1-unit': "g"
        }
        _ingredients = defs.ingredientsBuilder(_groupedKeys, _requestform)
        self.assertIsNotNone(_ingredients)
        self.assertEqual(_ingredients, {})

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
    def test_callRoot_expect200(self):
        self.app = app.test_client()
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_callHome_expect200(self):
        self.app = app.test_client()
        response = self.app.get("/home")
        self.assertEqual(response.status_code, 200)

    def test_callRegister_expect200(self):
        self.app = app.test_client()
        requestform = {
            "username": "test_user",
            "password": "test_pass",
            "email": "test@testy.com",
            "first_name": "test",
            "last_name": "testington",
            "dob": "01/01/2013",
            "country": "Testville",
        }

        response = self.app.post(
            "/register", data=requestform, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_callLogin_expect200(self):
        self.app = app.test_client()
        requestform = {
            "username": "test_user",
            "password": "test_pass",
        }

        response = self.app.post(
            "/login", data=requestform, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_callSearch_expect200(self):
        self.app = app.test_client()
        response = self.app.get("recipes/search")
        self.assertEqual(response.status_code, 200)

    def test_callRecipeBuilder_expect302(self):
        self.app = app.test_client()
        response = self.app.get("/recipe/builder")
        self.assertEqual(response.status_code, 302)

    def test_callAddRecipe_expect302(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user'] = 'test_user'
                sess['_fresh'] = True
            resp = c.post("/recipe/add", data={})
            self.assertEqual(resp.status_code, 302)

    def test_callPreviewRecipe_expect200(self):
        requestform = {
            "title": "test",
            "desc": "test desc",
            "portions": 4,
            "min": 1,
            "max": 72,
            "step-1-desc": "test_step",
            "step-1-type": "prepare",
            "step-1-time": 5,
        }
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user'] = 'test_user'
                sess['_fresh'] = True
            resp = c.post("/recipe/preview", data=requestform)
            self.assertEqual(resp.status_code, 200)

    def test_callEditRecipe_expect500(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user'] = 'test_user'
                sess['_fresh'] = True
            resp = c.post(
                "/recipe/edit", data={"_id": "111"})
            self.assertEqual(resp.status_code, 500)

    def test_callFavouriteRecipe_expect302(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user'] = 'some_fake_user'
                sess['_fresh'] = True
            resp = c.post(
                "/recipe/favourite", data={})
            self.assertEqual(resp.status_code, 302)

    def test_callLogout_expect302(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user'] = 'some_fake_user'
                sess['_fresh'] = True
            resp = c.get("/logout")
            self.assertEqual(resp.status_code, 302)


if __name__ == '__main__':
    unittest.main()
