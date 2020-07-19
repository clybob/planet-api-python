from flask import jsonify, request, Response

from api.app import app
from api.models import Planet, db
from api.swapi import Swapi


@app.route('/planets/', methods=['GET'])
def get_planets():
    search = request.args.get('search')
    results = []

    if search:
        planet_id = get_id_from_search(search)

        if planet_id:
            planets = Planet.query.filter_by(id=planet_id)
        else:
            planets = Planet.query.filter_by(name=search)
    else:
        planets = Planet.query.all()

    for planet in planets:
        results.append({
            'name': planet.name,
            'climate': planet.climate,
            'terrain': planet.terrain,
            'films_count': Swapi.get_planet_films(planet.name)
        })

    return jsonify(
        count=len(results),
        next=None,
        previous=None,
        results=results
    )


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

    return Response("", status=201, mimetype='application/json')


def get_id_from_search(search):
    try:
        planet_id = int(search)
    except ValueError:
        planet_id = None

    return planet_id
