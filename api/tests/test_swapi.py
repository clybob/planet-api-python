import unittest
import requests

from unittest.mock import patch

from api.swapi import Swapi


class TestSwapi(unittest.TestCase):

    def test_get_planet_films_should_return_0_when_planet_not_found(self):
        films_count = Swapi.get_planet_films('Terra2')
        self.assertEqual(films_count, 0)

    @patch('api.swapi.requests.get')
    def test_get_planet_films_should_return_0_when_api_is_out(self, mock):
        mock.return_value = self._fake_500_response()
        films_count = Swapi.get_planet_films('Tatooine')
        self.assertEqual(films_count, 0)

    def test_get_planet_films_should_return_number_of_films(self):
        films_count = Swapi.get_planet_films('Tatooine')
        self.assertEqual(films_count, 5)

    def _fake_500_response(self):
        r = requests.Response()
        r.status_code = 500
        return r
