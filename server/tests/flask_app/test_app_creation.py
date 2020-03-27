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


def test_app_is_testing(flask_app):
    """Test that the correct configurations
    are set when the app is configured for
    testing.
    """
    assert flask_app.config["TESTING"] is True
    assert flask_app.config["CSRF_ENABLED"] is True
    assert flask_app.config["JWT_IDENTITY_CLAIM"] == "sub"
    assert flask_app.config["JWT_ERROR_MESSAGE_KEY"] == "message"
    assert flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] == 1800
    assert flask_app.config["SECRET_KEY"] == "fake key for development only"
    assert flask_app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"
    assert flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False


