from flask_sqlalchemy import SQLAlchemy

from api.app import app
from api.manage import create_db

db = SQLAlchemy(app)


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    climate = db.Column(db.String(64), nullable=False)
    terrain = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Planet {name}>'.format(name=self.name)

app.cli.add_command(create_db(db))
