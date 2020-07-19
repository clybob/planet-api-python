from flask import jsonify, request


from api.app import app
from api.models import Planet
from api.swapi import Swapi


@app.route('/planets/', methods=['GET', 'POST'])
def planets():
    search = request.args.get('search')
    results = []

    if search:
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
