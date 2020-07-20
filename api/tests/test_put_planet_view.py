import json
import unittest

from unittest.mock import patch

from api.app import app
from api.models import Planet, db


class TestUpdatePlanetView(unittest.TestCase):
    planet_updated = {
        'name': 'Terra 2',
        'terrain': 'mountains',
        'climate': 'temperate'
    }

    def setUp(self):
        self.test_app = app.test_client()
        self._install_fixtures()

    def tearDown(self):
        self._delete_fixtures()

    def test_update_planet_should_return_ok(self):
        response = self._update_planet(self.planet1.id, self.planet_updated)
        self.assertEqual(response.status_code, 200)

    def test_update_planet_should_return_ok_when_is_partial(self):
        response = self._update_planet(self.planet1.id, {'name': 'Terra 2'})
        self.assertEqual(response.status_code, 200)

    def test_update_planet_should_return_json(self):
        response = self._update_planet(self.planet1.id, self.planet_updated)
        self.assertEqual(response.content_type, 'application/json')

    def test_update_planet_should_return_the_planet(self):
        response = self._update_planet(self.planet1.id, self.planet_updated)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {
            'id': self.planet1.id,
            'name': self.planet_updated['name'],
            'climate': self.planet_updated['climate'],
            'terrain': self.planet_updated['terrain'],
            'films_count': 2
        })

    def test_update_planet_should_return_not_found_when_id_is_wrong(self):
        response = self._update_planet(9999, self.planet_updated)
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['name'], 'Not Found')
        self.assertIn('not found', data['description'])

    def _install_fixtures(self):
        self.planet1 = Planet(name='Tatooine', climate='arid', terrain='desert')
        self.planet2 = Planet(name='Alderaan', climate='temperate', terrain='grasslands, mountains')

        db.session.add(self.planet1)
        db.session.commit()

    def _delete_fixtures(self):
        Planet.query.delete()
        db.session.commit()

    @patch('api.swapi.Swapi.get_planet_films')
    def _update_planet(self, planet_id, data, mock):
        mock.return_value = self._fake_update_planet_films()
        url = '/planets/{planet_id}/'.format(planet_id=planet_id)

        response = self._update(url, data=data)
        return response

    def _fake_update_planet_films(self):
        return 2

    def _update(self, url, data):
        return self.test_app.put(url, data=data)


class TestPatchPlanetView(TestUpdatePlanetView):
    # This class execute the same tests of put in patch version

    def _update(self, url, data):
        return self.test_app.patch(url, data=data)
