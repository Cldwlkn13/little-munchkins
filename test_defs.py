from app_definitions import AppDefinitions
from app import app
import unittest

app.testing = True
defs = AppDefinitions()


class TestDefs(unittest.TestCase):
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

    

    # Testing http endpoints
    def test_callHome(self):
        self.app = app.test_client()
        response = self.app.get("/")
        print(response)


if __name__ == '__main__':
    unittest.main()

