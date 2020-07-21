import json

from werkzeug.exceptions import HTTPException, BadRequest
from flask import request, Response, url_for

from api.app import app, cache
from api.models import Planet, PlanetSerializer, db


@app.route('/planets/', methods=['GET'])
def get_planets():
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)

    cache_key = 'get_planets_{search}_{page}'.format(search=search, page=page)
    if cache.get(cache_key):
        app.logger.info('CACHE HIT: GET /planets/.')
        response = cache.get(cache_key)
        return Response(response, status=200, mimetype='application/json')

    planets = get_filtered_planets(search)
    planets_page = planets.paginate(page, app.config['POSTS_PER_PAGE'], False)
    results = [PlanetSerializer(planet).data for planet in planets_page.items]

    response = json.dumps({
        'count': planets.count(),
        'next': get_paginate_url(planets_page, 'next'),
        'previous': get_paginate_url(planets_page, 'prev'),
        'results': results
    })

    cache.set(cache_key, response, timeout=30)
    app.logger.info('CACHE MISS: GET /planets/.')
    return Response(response, status=200, mimetype='application/json')


@app.route('/planets/', methods=['POST'])
def post_planets():
    fields = ['name', 'terrain', 'climate']
    new_planet_data = {}

    for field in fields:
        if field not in request.json:
            raise BadRequest("KeyError: '{key}'".format(key=field))

        new_planet_data[field] = request.json[field]

    new_planet = Planet(**new_planet_data)
    db.session.add(new_planet)
    db.session.commit()

    return Response(
        PlanetSerializer(new_planet).to_json(),
        status=201,
        mimetype='application/json'
    )


@app.route('/planets/<int:planet_id>/', methods=['GET'])
@cache.cached(timeout=30)
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return Response(
        PlanetSerializer(planet).to_json(),
        status=200,
        mimetype='application/json'
    )


@app.route('/planets/<int:planet_id>/', methods=['PUT', 'PATCH'])
def update_planet(planet_id):
    fields = ['name', 'terrain', 'climate']
    planet = Planet.query.get_or_404(planet_id)

    for field in fields:
        if request.json.get(field):
            setattr(planet, field, request.json[field])

    db.session.add(planet)
    db.session.commit()

    return Response(
        PlanetSerializer(planet).to_json(),
        status=200,
        mimetype='application/json'
    )


@app.route('/planets/<int:planet_id>/', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(json.dumps({}), status=204, mimetype='application/json')


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    app.logger.info('HTTP Exception: code {code} - {description}.'.format(
        code=e.code, description=e.description))

    response.data = json.dumps({
        'code': e.code,
        'name': e.name,
        'description': e.description,
    })
    response.content_type = 'application/json'
    return response


def get_filtered_planets(search):
    if search:
        planet_id = get_id_from_search(search)

        if planet_id:
            planets = Planet.query.filter_by(id=planet_id)
        else:
            planets = Planet.query.filter_by(name=search)
    else:
        planets = Planet.query

    return planets


def get_id_from_search(search):
    try:
        planet_id = int(search)
    except ValueError:
        planet_id = None

    return planet_id


def get_paginate_url(planets, direction):
    if getattr(planets, 'has_{direction}'.format(direction=direction), None):
        return url_for(
            'get_planets',
            page=getattr(planets, '{direction}_num'.format(direction=direction)),
            _external=True
        )
