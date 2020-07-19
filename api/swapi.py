import requests

from api.app import app


class Swapi(object):
    @classmethod
    def get_planet_films(cls, name):
        url = 'https://swapi.dev/api/planets/?search={name}'.format(name=name)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data['count'] == 0:
                app.logger.info('Swapi: Planet does not exists.')
                return data['count']
