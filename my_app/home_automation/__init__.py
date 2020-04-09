
from flask import Flask
from .celery_conf import make_celery
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)


# Config options - Make sure you created a 'config.py' file.
flask_app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

celery = make_celery(flask_app)

db = SQLAlchemy(flask_app)
# importing views after initiation of flask_app to avoid circular import
from . import views


