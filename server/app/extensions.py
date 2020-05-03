"""This module contains all of the extensions for the application."""


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from celery import Celery


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()
celery = Celery()

