import unittest

from api.swapi import Swapi


class TestSwapi(unittest.TestCase):

    def test_get_planet_films_should_return_0_when_planet_not_found(self):
        films_count = Swapi.get_planet_films('Terra2')
        self.assertEqual(films_count, 0)
