"""This module contains pytest fixtures to be used in testing the application."""


import pytest
import json as json_module
from app import create_app
from app.models import User
from flask_app.utils import AuthActions, generate_user_instance


@pytest.fixture
def flask_app():
    """Fixture for the application instance with testing configurations."""
    app = create_app(config_name="testing")
    from app.extensions import db

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def db(flask_app):
    """Fixture for the database."""
    from app.extensions import db as db_instance
    yield db_instance
    

@pytest.fixture
def flask_test_client(flask_app):
    """Fixture for the Flask test client."""
    return flask_app.test_client()


@pytest.fixture
def auth(flask_test_client):
    """Fixture to authenicate with the api."""
    return AuthActions(flask_test_client)


@pytest.fixture
def user(db):
    """Fixture that adds a user to the database
    and then returns the user instance.
    """
    new_user = User(
        id=1,
        username="test user", 
        password="password",
        email="testuser@gmail.com"
    )
    return new_user
    

@pytest.fixture
def token(user, auth, db):
    """Fixture to register a test user and return a JWT, which is necessary
    for accessing the api endpoints."""
    token = auth.register(
        username=user.username, password="password", email=user.email
    )
    return token


@pytest.fixture
def json():
    """Fixture that makes use of the json module for serializing
    and deserializing data.
    """
    return json_module



