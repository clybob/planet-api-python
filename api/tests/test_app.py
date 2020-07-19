import json
import unittest

from unittest.mock import patch

from api.app import app
from api.models import Planet, db


class TestPlanetsView(unittest.TestCase):
    maxDiff = 1000

    def setUp(self):
        self.test_app = app.test_client()
        self._install_fixtures()

    def tearDown(self):
        self._delete_fixtures()

    def test_put_planets_should_return_not_implemented(self):
        response = self.test_app.put('/planets')
        self.assertEqual(response.status_code, 405)

    def test_delete_planets_should_return_not_implemented(self):
        response = self.test_app.delete('/planets')
        self.assertEqual(response.status_code, 405)

    def test_get_planets_should_return_ok(self):
        response = self._get_planets()
        self.assertEqual(response.status_code, 200)

    def test_get_planets_should_return_json(self):
        response = self._get_planets()
        self.assertIn(response.content_type, 'application/json')

    def test_get_planets_should_return_a_list_of_planets(self):
        response = self._get_planets()
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'name': self.planet1.name,
                    'climate': self.planet1.climate,
                    'terrain': self.planet1.terrain,
                    'films_count': 2
                },
                {
                    'name': self.planet2.name,
                    'climate': self.planet2.climate,
                    'terrain': self.planet2.terrain,
                    'films_count': 2
                }
            ]
        })

    def _install_fixtures(self):
        self.planet1 = Planet(name='Tatooine', climate='arid', terrain='desert')
        self.planet2 = Planet(name='Alderaan', climate='temperate', terrain='grasslands, mountains')

        db.session.add(self.planet1)
        db.session.add(self.planet2)
        db.session.commit()

    def _delete_fixtures(self):
        Planet.query.delete()

    @patch('api.swapi.Swapi.get_planet_films')
    def _get_planets(self, mock):
        mock.return_value = self._fake_get_planet_films()
        response = self.test_app.get('/planets')
        return response

    def _fake_get_planet_films(self):
        return 2
