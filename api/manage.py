import click
from flask.cli import with_appcontext


def create_db(db):
    @click.command(name='create-db')
    @with_appcontext
    def run_create_db():
        db.drop_all()
        db.create_all()

    return run_create_db
