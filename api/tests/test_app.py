import unittest

from api.app import app


class TestPlanetsView(unittest.TestCase):

    def setUp(self):
        self.test_app = app.test_client()

    def test_put_planets_should_return_not_implemented(self):
        self.response = self.test_app.put('/planets')
        self.assertEqual(self.response.status_code, 405)

    def test_delete_planets_should_return_not_implemented(self):
        self.response = self.test_app.delete('/planets')
        self.assertEqual(self.response.status_code, 405)

    def test_get_planets_should_return_ok(self):
        self.response = self.test_app.get('/planets')
        self.assertEqual(self.response.status_code, 200)


