import unittest

from api.app import app


class TestPostPlanetsView(unittest.TestCase):
    maxDiff = 1000
    planet = {
        'name': 'test',
        'terrain': 'test',
        'climate': 'test'
    }

    def setUp(self):
        self.test_app = app.test_client()

    def test_post_planets_should_return_created(self):
        response = self._post_planets(self.planet)
        self.assertEqual(response.status_code, 201)

    def test_post_planets_should_return_json(self):
        response = self._post_planets(self.planet)
        self.assertIn(response.content_type, 'application/json')

    def _post_planets(self, data):
        url = '/planets/'
        response = self.test_app.post(url, data=data)

        return response
