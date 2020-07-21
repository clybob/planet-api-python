import json
import unittest

from unittest.mock import patch

from api.app import app, cache
from api.models import Planet, db


class TestGetPlanetsView(unittest.TestCase):
    maxDiff = 1000

    def setUp(self):
        self.test_app = app.test_client()
        self._install_fixtures()

    def tearDown(self):
        self._delete_fixtures()

    def test_get_planets_should_return_ok(self):
        response = self._get_planets()
        self.assertEqual(response.status_code, 200)

    def test_get_planets_should_return_json(self):
        response = self._get_planets()
        self.assertEqual(response.content_type, 'application/json')

    def test_get_planets_should_return_a_list_of_planets(self):
        response = self._get_planets()
        data = json.loads(response.get_data(as_text=True))

        self.assertPaginate(data, count=2, results=2)
        self.assertEqual(data['results'], [
            {
                'id': self.planet1.id,
                'name': self.planet1.name,
                'climate': self.planet1.climate,
                'terrain': self.planet1.terrain,
                'films_count': 2
            },
            {
                'id': self.planet2.id,
                'name': self.planet2.name,
                'climate': self.planet2.climate,
                'terrain': self.planet2.terrain,
                'films_count': 2
            }
        ])

    def test_get_planets_should_return_cached(self):
        self._get_planets()

        with patch('json.dumps') as mock:
            mock.return_value = {}
            self._get_planets()
            self.assertFalse(mock.called)

    def test_get_planets_should_return_an_empty_list_of_planets(self):
        self._delete_fixtures()
        cache.delete('get_planets_None_1')
        response = self._get_planets()
        data = json.loads(response.get_data(as_text=True))

        self.assertPaginate(data, count=0, results=0)
        self.assertEqual(data['results'], [])

    def test_get_planets_should_return_filtered_planets_by_name(self):
        response = self._get_planets(search='Tatooine')
        data = json.loads(response.get_data(as_text=True))

        self.assertPaginate(data, count=1, results=1)
        self.assertEqual(data['results'], [{
            'id': self.planet1.id,
            'name': self.planet1.name,
            'climate': self.planet1.climate,
            'terrain': self.planet1.terrain,
            'films_count': 2
        }])

    def test_get_planets_should_return_filtered_planets_by_id(self):
        response = self._get_planets(search=self.planet2.id)
        data = json.loads(response.get_data(as_text=True))

        self.assertPaginate(data, count=1, results=1)
        self.assertEqual(data['results'], [{
            'id': self.planet2.id,
            'name': self.planet2.name,
            'climate': self.planet2.climate,
            'terrain': self.planet2.terrain,
            'films_count': 2
        }])

    def test_get_planets_should_return_a_list_with_pagination(self):
        cache.delete('get_planets_None_1')
        self._create_planets()

        response = self._get_planets()
        data = json.loads(response.get_data(as_text=True))

        expected_next_url = 'http://localhost:5000/planets/?page=2'
        self.assertPaginate(data, count=22, results=20, next_url=expected_next_url)

    def test_get_planets_should_return_planets_of_page_2(self):
        cache.delete('get_planets_None_1')
        self._create_planets()

        response = self._get_planets(page=2)
        data = json.loads(response.get_data(as_text=True))

        expected_previous_url = 'http://localhost:5000/planets/?page=1'
        self.assertPaginate(data, count=22, results=2, previous_url=expected_previous_url)

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
    def _get_planets(self, mock, search=None, page=None):
        mock.return_value = self._fake_get_planet_films()
        url = '/planets/'

        if search:
            url += '?search={search}'.format(search=search)

        if page:
            url += '?page={page}'.format(page=page)

        response = self.test_app.get(url)

        return response

    def _fake_get_planet_films(self):
        return 2

    def _create_planets(self, total=20):
        for x in range(0, total):
            test_data = 'Terra {x}'.format(x=x)
            new_planet = Planet(name=test_data, climate=test_data, terrain=test_data)
            db.session.add(new_planet)

        db.session.commit()

    def assertPaginate(self, data, count=0, results=0, next_url=None, previous_url=None):
        self.assertEqual(data['count'], count)
        self.assertEqual(len(data['results']), results)
        self.assertEqual(data['previous'], previous_url)
        self.assertEqual(data['next'], next_url)
