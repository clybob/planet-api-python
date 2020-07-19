import json
import unittest

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
        response = self.test_app.get('/planets')
        self.assertEqual(response.status_code, 200)

    def test_get_planets_should_return_json(self):
        response = self.test_app.get('/planets')
        self.assertIn(response.content_type, 'application/json')

    def test_get_planets_should_return_a_list_of_planets(self):
        response = self.test_app.get('/planets')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'name': 'Tatooine',
                    'climate': 'arid',
                    'terrain': 'desert',
                    'films_count': 5
                },
                {
                    'name': 'Alderaan',
                    'climate': 'temperate',
                    'terrain': 'grasslands, mountains',
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
