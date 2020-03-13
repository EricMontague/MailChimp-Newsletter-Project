"""This module contains different configuration classes for the application."""


import os


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Base class for application configuration"""

    # stored in a .flaskenv file
    # hard to guess string is used only for development.
    # A real key is generated for production
    SECRET_KEY = os.environ.get("SECRET KEY", "hard to guess string")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    """Class to setup the development configuration for the application"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


class TestingConfig(BaseConfig):
    """Class to setup the testing configuration for the application"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"


class ProductionConfig(BaseConfig):
    """Class to setop the production configuration for the application"""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}


