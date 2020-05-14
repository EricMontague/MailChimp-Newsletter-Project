"""This module contains the functions for creating an confiuring the
application instance.
"""


import os
from flask import Flask
from config import CONFIG_NAME_MAPPER
from app.extensions import db, ma, migrate, jwt


def create_app(config_name):
    """Factory function for the application instance."""
    app = Flask(__name__.split('.')[0])
    app.config.from_object(CONFIG_NAME_MAPPER[config_name])
    configure_extensions(app)
    register_blueprints(app)
    return app


def configure_extensions(app):
    """Configure Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app):
    """Register all blueprints for the application."""
    from app.api.views import api_blueprint
    from app.auth.views import auth_blueprint
    from app.mailchimp.views import mailchimp_blueprint
    app.register_blueprint(api_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(mailchimp_blueprint)


