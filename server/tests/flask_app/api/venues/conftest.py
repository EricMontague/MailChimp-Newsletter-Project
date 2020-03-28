"""This module contains fixtures for running tests on the venue endpoints."""


from app.models import Venue
import pytest


@pytest.fixture
def venue(db):
    """Fixture to represent a venue."""
    venue = Venue(
        name="Eric's Jazzhaus",
        street_address="400 S. Broad St.",
        city="Philadelphia",
        state="PA",
        zip_code="19121"
    )
    db.session.add(venue)
    db.session.commit()
    return venue

