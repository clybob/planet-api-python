import json

from werkzeug.exceptions import HTTPException
from flask import request, Response, url_for

from api.app import app, cache
from api.models import Planet, PlanetSerializer, db


@app.route('/planets/', methods=['GET'])
def get_planets():
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)

    cache_key = 'get_planets_{search}'.format(search=search)
    if cache.get(cache_key):
        app.logger.info('CACHE HIT: GET /planets/.')
        response = cache.get(cache_key)
        return Response(response, status=200, mimetype='application/json')

    if search:
        planet_id = get_id_from_search(search)

        if planet_id:
            planets = Planet.query.filter_by(id=planet_id)
        else:
            planets = Planet.query.filter_by(name=search)
    else:
        planets = Planet.query

    count = planets.count()

    planets = planets.paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('get_planets', page=planets.next_num, _external=True) if planets.has_next else None
    prev_url = url_for('get_planets', page=planets.prev_num, _external=True) if planets.has_prev else None

    results = [PlanetSerializer(planet).data for planet in planets.items]

    response = json.dumps({
        'count': count,
        'next': next_url,
        'previous': prev_url,
        'results': results
    })

    cache.set(cache_key, response, timeout=30)
    app.logger.info('CACHE MISS: GET /planets/.')
    return Response(response, status=200, mimetype='application/json')


@app.route('/planets/', methods=['POST'])
def post_planets():
    new_planet_data = {
        'name': request.form['name'],
        'terrain': request.form['terrain'],
        'climate': request.form['climate']
    }

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
    planet = Planet.query.get_or_404(planet_id)

    if request.form.get('name'):
        planet.name = request.form['name']

    if request.form.get('terrain'):
        planet.terrain = request.form['terrain']

    if request.form.get('climate'):
        planet.climate = request.form['climate']

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


def get_id_from_search(search):
    try:
        planet_id = int(search)
    except ValueError:
        planet_id = None

    return planet_id
