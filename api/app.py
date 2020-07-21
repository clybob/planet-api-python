import os

from flask import Flask
from flask_caching import Cache

config = {
    'DEBUG': True,
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 1
}

app = Flask(__name__)
app.config['SERVER_NAME'] = os.environ['SERVER_NAME']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['POSTS_PER_PAGE'] = 20

app.config.from_mapping(config)
cache = Cache(app)

from api import models
from api import views
