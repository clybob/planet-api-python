import unittest

from api.app import app


class TestBasePlanetsView(unittest.TestCase):
    url = '/planets/'
    test_app = app.test_client()

    def test_put_planets_should_return_not_implemented(self):
        response = self.test_app.put(self.url)
        self.assertEqual(response.status_code, 405)

    def test_delete_planets_should_return_not_implemented(self):
        response = self.test_app.delete(self.url)
        self.assertEqual(response.status_code, 405)
