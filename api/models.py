import json

from flask_sqlalchemy import SQLAlchemy

from api.app import app
from api.manage import create_db
from api.swapi import Swapi

db = SQLAlchemy(app)


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    climate = db.Column(db.String(64), nullable=False)
    terrain = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Planet {name}>'.format(name=self.name)


class PlanetSerializer(object):
    def __init__(self, planet):
        self.data = {
            'id': planet.id,
            'name': planet.name,
            'climate': planet.climate,
            'terrain': planet.terrain,
            'films_count': Swapi.get_planet_films(planet.name)
        }

    def to_json(self):
        return json.dumps(self.data)

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )


app.cli.add_command(create_db(db))
