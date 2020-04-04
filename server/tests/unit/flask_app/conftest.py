"""This module contains fixtures for unit tests."""

"""This module contains pytest fixtures to be used in testing the application."""


import pytest
from app import create_app
from app.models import User


@pytest.fixture
def user():
    """Fixture that adds a user to the database
    and then returns the user instance.
    """
    new_user = User(
        id=1, username="test user", password="password", email="testuser@gmail.com"
    )
    return new_user

