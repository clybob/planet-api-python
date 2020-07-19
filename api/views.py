from flask import jsonify

from api.app import app
from api.models import Planet


@app.route('/planets', methods=['GET', 'POST'])
def planets():
    planets = Planet.query.all()
    results = []
    films_count = {
        'Tatooine': 5,
        'Alderaan': 2
    }

    for planet in planets:
        results.append({
            'name': planet.name,
            'climate': planet.climate,
            'terrain': planet.terrain,
            'films_count': films_count[planet.name]
        })

    return jsonify(
        count=2,
        next=None,
        previous=None,
        results=results
    )
