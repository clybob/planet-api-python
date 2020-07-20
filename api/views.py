import json

from werkzeug.exceptions import HTTPException
from flask import request, Response

from api.app import app, cache
from api.models import Planet, PlanetSerializer, db


@app.route('/planets/', methods=['GET'])
def get_planets():
    search = request.args.get('search')
    results = []

    cache_key = 'get_planets_{search}'.format(search=search)
    if cache.get(cache_key):
        response = cache.get(cache_key)
        return Response(response, status=200, mimetype='application/json')

    if search:
        planet_id = get_id_from_search(search)

        if planet_id:
            planets = Planet.query.filter_by(id=planet_id)
        else:
            planets = Planet.query.filter_by(name=search)
    else:
        planets = Planet.query.all()

    for planet in planets:
        results.append(PlanetSerializer(planet).data)

    response = json.dumps({
        'count': len(results),
        'next': None,
        'previous': None,
        'results': results
    })

    cache.set(cache_key, response, timeout=30)
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


def get_id_from_search(search):
    try:
        planet_id = int(search)
    except ValueError:
        planet_id = None

    return planet_id


@app.errorhandler(HTTPException)
def handle_bad_request(e):
    response = e.get_response()

    response.data = json.dumps({
        'code': e.code,
        'name': e.name,
        'description': e.description,
    })
    response.content_type = 'application/json'
    return response
