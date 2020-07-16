import unittest

from api.app import app


class TestPlanetsView(unittest.TestCase):

    def setUp(self):
        self.test_app = app.test_client()

    def test_get_planets_should_return_ok(self):
        self.response = self.test_app.get('/planets')
        self.assertEqual(self.response.status_code, 200)
