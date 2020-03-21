"""This module contains different configuration classes for the application."""


import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Base class for application configuration"""

    SECRET_KEY = "fake key for development only"
    JWT_IDENTITY_CLAIM = "sub"
    JWT_ERROR_MESSAGE_KEY = "message"
    JWT_ACCESS_TOKEN_EXPIRES = 1800
    DB_USER = "ericmontague"
    DB_PASSWORD = "password"
    DB_NAME = "mailchimp_project"
    DB_HOST = "localhost"
    DB_PORT = 5432
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    CSRF_ENABLED = True #check later to see if this is really needed
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    """Class to setup the development configuration for the application"""

    DEBUG = True
 

class TestingConfig(BaseConfig):
    """Class to setup the testing configuration for the application"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class ProductionConfig(BaseConfig):
    """Class to setop the production configuration for the application"""

    SECRET_KEY = os.environ.get("SECRET_KEY")


CONFIG_NAME_MAPPER = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}


