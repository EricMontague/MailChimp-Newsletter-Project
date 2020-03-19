"""This module contains pytest fixtures to be used in testing the API endpoints."""


import pytest
from app import create_app


@pytest.fixture
def flask_app():
    """Fixture for the application instance."""
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
