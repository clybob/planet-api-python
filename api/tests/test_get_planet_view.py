import json
import unittest

from unittest.mock import patch

from api.app import app
from api.models import Planet, db


class TestGetPlanetView(unittest.TestCase):
    maxDiff = 1000

    def setUp(self):
        self.test_app = app.test_client()
        self._install_fixtures()

    def tearDown(self):
        self._delete_fixtures()

    def test_get_planet_should_return_ok(self):
        response = self._get_planet(self.planet1.id)
        self.assertEqual(response.status_code, 200)

    def test_get_planet_should_return_json(self):
        response = self._get_planet(self.planet1.id)
        self.assertEqual(response.content_type, 'application/json')

    def test_get_planet_should_return_the_planet(self):
        response = self._get_planet(self.planet1.id)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {
            'id': self.planet1.id,
            'name': self.planet1.name,
            'climate': self.planet1.climate,
            'terrain': self.planet1.terrain,
            'films_count': 2
        })

    def test_get_planet_should_return_does_not_found_when_id_is_wrong(self):
        response = self._get_planet(9999)
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['name'], 'Not Found')
        self.assertIn('not found', data['description'])

    def _install_fixtures(self):
        self.planet1 = Planet(name='Tatooine', climate='arid', terrain='desert')
        self.planet2 = Planet(name='Alderaan', climate='temperate', terrain='grasslands, mountains')

        db.session.add(self.planet1)
        db.session.add(self.planet2)
        db.session.commit()

    def _delete_fixtures(self):
        Planet.query.delete()
        db.session.commit()

    @patch('api.swapi.Swapi.get_planet_films')
    def _get_planet(self, planet_id, mock):
        mock.return_value = self._fake_get_planet_films()
        url = '/planets/{planet_id}/'.format(planet_id=planet_id)

        response = self.test_app.get(url)
        return response

    def _fake_get_planet_films(self):
        return 2
