"""This module contains the functions for creating an confiuring the
application instance.
"""


from flask import Flask
from config import config
from .extensions import db, ma, migrate


def create_app(config_name):
    """Factory function for the application instance."""
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config[config_name])
    configure_extensions(app)
    register_blueprints(app)
    return app


def configure_extensions(app):
    """Configure Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    """Register all blueprints for the application."""
    from .api.views import api_blueprint
    app.register_blueprint(api_blueprint)
