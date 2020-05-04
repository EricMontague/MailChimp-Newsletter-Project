"""This module contains the functions for creating an confiuring the
application instance.
"""


import os
from flask import Flask
from config import CONFIG_NAME_MAPPER
from app.extensions import db, ma, migrate, jwt, celery


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
    from .api.views import api_blueprint
    from .auth.views import auth_blueprint
    app.register_blueprint(api_blueprint)
    app.register_blueprint(auth_blueprint)


def init_celery(app=None):
    """Return a Celery instance after setting up its configurations."""
    from celery.schedules import crontab
    app = app or create_app(os.environ.get("FLASK_CONFIG") or "default")
    celery.name = __name__
    celery.conf.update(app.config)
    celery.conf.beat_schedule = {
        "crawl-every-sunday-morning": {
            "task": "app.scrapy.performance_scraper.tasks.scheduled_crawl",
            "schedule": crontab(hour=9, minute=0, day_of_week=0),
            "args": []
        }
    }


    class ContextTask(celery.Task):
        """Make celery tasks work within the Flask app context."""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    

    celery.Task = ContextTask
    return celery

