import unittest

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
        self.assertIn(response.content_type, 'application/json')

    def test_post_planets_should_save_planet_on_db(self):
        self._post_planets(self.planet)
        test_planet = Planet.query.first()

        self.assertEqual(test_planet.name, 'test')
        self.assertEqual(test_planet.terrain, self.planet['terrain'])
        self.assertEqual(test_planet.climate, self.planet['climate'])

    def _post_planets(self, data):
        url = '/planets/'
        response = self.test_app.post(url, data=data)

        return response
