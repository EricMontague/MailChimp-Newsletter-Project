"""This module is for testing that the application instance is
successfully created and configured properly.
"""


import pytest
from app import create_app


@pytest.mark.parametrize("config_name", ["production", "development", "testing"])
def test_create_app_passing_config_name(config_name):
    """Test to ensure the successfully creation of the application
    instance.
    """
    assert create_app(config_name) is not None


def test_create_app_with_non_existing_config():
    """Test to ensure the application factory function
    throws an error when an incorrect configuration name
    is passed in.
    """
    with pytest.raises(KeyError):
        create_app("wrong_config_name")


def test_app_is_development(flask_app_development):
    """Test that the correct configurations
    are set when the app is configured for
    development.
    """
    assert flask_app_development.config["DEBUG"] is True
    assert flask_app_development.config["SECRET_KEY"] == "fake key for development only"
    assert flask_app_development.config["JWT_SECRET_KEY"] == "another fake key for development only"
    assert flask_app_development.config["SQLALCHEMY_DATABASE_URI"] == (
        f"postgresql://ericmontague:password@localhost:5432/mailchimp_project"
    )


def test_app_is_testing(flask_app_testing):
    """Test that the correct configurations
    are set when the app is configured for
    testing.
    """
    assert flask_app_testing.config["TESTING"] is True
    assert flask_app_development.config["SECRET_KEY"] == "fake key for development only"
    assert flask_app_development.config["JWT_SECRET_KEY"] == "another fake key for development only"
    assert flask_app_testing.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"


