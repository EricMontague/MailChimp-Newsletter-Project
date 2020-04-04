"""This module contains pytest fixtures to be used in testing the application."""


import pytest
from datetime import datetime
import json as json_module
from app import create_app
from app.models import User, Venue, Image, Artist, Performance
from flask_app.utils import AuthActions #need to fix this so it's not relative


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
        id=1, username="test user", password="password", email="testuser@gmail.com"
    )
    return new_user


@pytest.fixture
def artist(db):
    """Fixture that adds an artist to the database
    and then returns the artist instance.
    """
    artist = Artist(
        name="test artist", bio="test bio", website="http://www.example.com"
    )
    db.session.add(artist)
    db.session.commit()
    return artist


@pytest.fixture
def image(db, artist):
    """Fixture that adds an image to the database
    and then returns the image instance.
    """
    image = Image(path="/Users/fakeuser/mailchimp_project/app/static", artist=artist)
    db.session.add(image)
    db.session.commit()
    return image


@pytest.fixture
def venue(db):
    """Fixture to represent a venue."""
    venue = Venue(
        name="Eric's Jazzhaus",
        street_address="400 S. Broad St.",
        city="Philadelphia",
        state="PA",
        zip_code="19121",
    )
    db.session.add(venue)
    db.session.commit()
    return venue


@pytest.fixture
def performance(db, artist, venue):
    """Fixture to represent a performance."""
    performance = Performance(
        title="test_title",
        description="test_description",
        url="http://www.jazzclub.com",
        start_datetime=datetime(2020, 4, 12, 10),
        end_datetime=datetime(2020, 4, 13, 10),
        artist=artist,
        venue=venue,
    )
    db.session.add(performance)
    db.session.commit()
    return performance


@pytest.fixture
def json():
    """Fixture that makes use of the json module for serializing
    and deserializing data.
    """
    return json_module

