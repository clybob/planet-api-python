import json
import unittest

from api.app import app
from api.models import Planet, db


class TestDeletePlanetView(unittest.TestCase):
    def setUp(self):
        self.test_app = app.test_client()
        self._install_fixtures()

    def tearDown(self):
        self._delete_fixtures()

    def test_delete_planet_should_return_ok(self):
        response = self._delete_planet(self.planet1.id)
        self.assertEqual(response.status_code, 204)

    def test_delete_planet_should_return_json(self):
        response = self._delete_planet(self.planet1.id)
        self.assertEqual(response.content_type, 'application/json')

    def test_delete_planet_should_return_empty_json(self):
        response = self._delete_planet(self.planet1.id)
        self.assertEqual(response.get_data(as_text=True), '')

    def test_delete_planet_should_return_not_found_when_id_is_wrong(self):
        response = self._delete_planet(9999)
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['name'], 'Not Found')
        self.assertIn('not found', data['description'])

    def _install_fixtures(self):
        self.planet1 = Planet(name='Tatooine', climate='arid', terrain='desert')

        db.session.add(self.planet1)
        db.session.commit()

    def _delete_fixtures(self):
        Planet.query.delete()
        db.session.commit()

    def _delete_planet(self, planet_id):
        url = '/planets/{planet_id}/'.format(planet_id=planet_id)
        response = self.test_app.delete(url)
        return response
