import json
import unittest

from unittest.mock import patch

from api.app import app
from api.models import Planet, db


class TestPostPlanetsView(unittest.TestCase):
    maxDiff = 1000
    planet = {
        'name': 'test',
        'terrain': 'test',
        'climate': 'test'
    }

    def setUp(self):
        self.test_app = app.test_client()

    def tearDown(self):
        Planet.query.delete()
        db.session.commit()

    def test_post_planets_should_return_created(self):
        response = self._post_planets(self.planet)
        self.assertEqual(response.status_code, 201)

    def test_post_planets_should_return_json(self):
        response = self._post_planets(self.planet)
        self.assertEqual(response.content_type, 'application/json')

    def test_post_planets_should_save_planet_on_db(self):
        self._post_planets(self.planet)
        test_planet = Planet.query.first()

        self.assertEqual(test_planet.name, 'test')
        self.assertEqual(test_planet.terrain, self.planet['terrain'])
        self.assertEqual(test_planet.climate, self.planet['climate'])

    def test_post_planets_should_return_planet(self):
        response = self._post_planets(self.planet)
        app.logger.info('dada' + response.get_data(as_text=True))
        data = json.loads(response.get_data(as_text=True))

        self.assertDictContainsSubset({
            'name': self.planet['name'],
            'climate': self.planet['climate'],
            'terrain': self.planet['terrain'],
            'films_count': 2
        }, data)

    def test_post_planets_should_return_bad_request_when_data_is_invalid(self):
        response = self._post_planets({'name': 'test'})
        self.assertEqual(response.status_code, 400)

    def test_post_planets_should_return_bad_request_details(self):
        response = self._post_planets({'name': 'test', 'terrain': 'test'})
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['code'], 400)
        self.assertEqual(data['name'], 'Bad Request')
        self.assertIn("KeyError: 'climate'", data['description'])

    @patch('api.swapi.Swapi.get_planet_films')
    def _post_planets(self, json, mock):
        mock.return_value = self._fake_update_planet_films()
        url = '/planets/'
        response = self.test_app.post(url, json=json)

        return response

    def _fake_update_planet_films(self):
        return 2
