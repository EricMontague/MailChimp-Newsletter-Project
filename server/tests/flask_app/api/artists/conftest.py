"""This module contains fixtures for tests for the artist endpoints."""


import pytest
from app.models import Artist


@pytest.fixture
def artist(db):
    """Fixture that adds an artist to the database
    and then returns the artist instance.
    """
    artist = Artist(
        name="test artist", 
        bio="test bio",
        website="http://www.example.com"
    )
    db.session.add(artist)
    db.session.commit()
    yield artist

    #Cleanup
    db.session.delete(artist)
