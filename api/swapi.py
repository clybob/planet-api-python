import requests

from api.app import app


class Swapi(object):
    @classmethod
    def get_planet_films(cls, name):
        url = 'https://swapi.dev/api/planets/?search={name}'.format(name=name)
        response = requests.get(url)

        if response.status_code == 200:
            return cls._get_films_count_from_valid_response(response)
        else:
            app.logger.error('Swapi: API Status Code: {code}.'.format(code=response.status_code))
            return 0

    @classmethod
    def _get_films_count_from_valid_response(cls, response):
        data = response.json()

        if data['count']:
            return len(data['results'][0]['films'])
        else:
            app.logger.info('Swapi: Planet does not exists.')
            return data['count']
