"""This module contains tests for modifying venue resources."""


from pytest import mark
from flask_app.utils import get_headers
from app.models import Venue


def test_create_new_venue_with_valid_data(flask_test_client, auth, user, json, db):
    """Test that a new venue resource can be succesfully created
    when valid data is sent to the api.
    """
    expected_fields = {
        "id", "name", "street_address", "city", "state", "zip_code", "performances", "_links"
    }
    new_venue = {
        "name": "South",
        "street_address": "1400 Broad. St.",
        "city": "Philadelphia",
        "state": "PA",
        "zip_code": "19212"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/venues",
        headers=get_headers(token),
        data=json.dumps(new_venue)
    )
    assert response.status == "201 CREATED"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == expected_fields
    assert response.json["id"] == 1
    assert response.json["name"] == new_venue["name"]
    assert response.json["street_address"] == new_venue["street_address"]
    assert response.json["city"] == new_venue["city"]
    assert response.json["state"] == new_venue["state"]
    assert response.json["zip_code"] == new_venue["zip_code"]
    assert response.json["performances"] == []
    assert response.json["_links"]["uri"] == "/api/v1/venues/1"
    assert response.json["_links"]["collection"] == "/api/v1/venues"


@mark.parametrize(
    "test_input, expected",
    [
        (
            {"street_address": "123 Main St.", "city": "New York", "state": "NY", "zip_code": "12345"},
            {"incorrect_field": "name", "message": ["Missing data for required field."]}
        ),
        (
            {"name": "Test Venue", "city": "New York", "state": "NY", "zip_code": "12345"},
            {"incorrect_field": "street_address", "message": ["Missing data for required field."]}
        ),
        (
            {"name": "Test Venue", "street_address": "123 Main St.", "state": "NY", "zip_code": "12345"},
            {"incorrect_field": "city", "message": ["Missing data for required field."]}
        ),
        (
            {"name": "Test Venue", "street_address": "123 Main St.", "city": "New York", "zip_code": "12345"},
            {"incorrect_field": "state", "message": ["Missing data for required field."]}
        ),
        (
            {"name": "Test Venue", "street_address": "123 Main St.", "state": "NY", "city": "New York"},
            {"incorrect_field": "zip_code", "message": ["Missing data for required field."]}
        )
    ]
)
def test_create_new_venue_missing_required_fields_must_fail(flask_test_client, auth, user, json, test_input, expected):
    """Test that a new venue resource cannot be created
    if required fields are missing.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/venues",
        headers=get_headers(token),
        data=json.dumps(test_input)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"][expected["incorrect_field"]] == expected["message"]

    venue = Venue.query.first()
    assert venue is None



@mark.parametrize(
    "test_input, expected",
    [
        (
            {"name": "", "street_address": "123 Main St.", "state": "NY", "city": "New York", "zip_code": "12345"},
            {"incorrect_field": "name", "message": ["Length must be between 1 and 64."]}
        ),
        (
            {"name": "Test Venue", "street_address": "123 Main St" * 10, "state": "NY", "city": "New York", "zip_code": "12345"},
            {"incorrect_field": "street_address", "message": ["Length must be between 1 and 64."]}
        ),
        (
            {"name": "Test Venue", "street_address": "123 Main St.", "state": "NAA", "city": "New York", "zip_code": "12345"},
            {"incorrect_field": "state", "message": ["Length must equal 2."]}
        ),
        (
            {"name": "Test Venue", "street_address": "123 Main St.", "state": "NY", "city": "", "zip_code": "12345"},
            {"incorrect_field": "city", "message": ["Length must be between 1 and 64."]}
        ),
        (
            {"name": "Test Venue", "street_address": "123 Main St.", "state": "NY", "city": "New York", "zip_code": None},
            {"incorrect_field": "zip_code", "message": ["Length must be between 5 and 10."]}
        )
    ]
)
def test_create_new_venue_with_incorrect_field_lengths_must_fail(flask_test_client, auth, user, json, test_input, expected):
    """Test that a new venue resource cannot be created
    if field lengths are incorrect.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/venues",
        headers=get_headers(token),
        data=json.dumps(test_input)
    )
    response.status == "400 BAD REQUEST"
    response.content_type == "application/json"
    response.json["message"][expected["incorrect_field"]] == expected["message"]



def test_create_new_venue_with_invalid_state_must_fail(flask_test_client, json, auth, user):
    """Test that a new venue resource cannot be created
    if an incorrect state is provided.
    """
    new_venue = {
        "name": "South",
        "street_address": "1400 Broad. St.",
        "city": "Philadelphia",
        "state": "PT",
        "zip_code": "19212"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/venues",
        headers=get_headers(token),
        data=json.dumps(new_venue)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"

    #should return a list of states that are valid to choose from
    assert isinstance(response.json["message"]["state"], list)

    venue = Venue.query.first()
    assert venue is None

    
@mark.parametrize(
    "test_input, expected",
    [
        (
            {"name": None, "street_address": "123 Main St.", "state": "NY", "city": "New York", "zip_code": "12345"},
            {"incorrect_field": "name", "message": ["Field may not be null."]}
        ),
        (
            {"name": "Test Venue", "street_address": None, "state": "NY", "city": "New York", "zip_code": "12345"},
            {"incorrect_field": "street_address", "message": ["Field may not be null."]}
        ),
        (
            {"name": "Test Venue", "street_address": "123 Main St.", "state": None, "city": "New York", "zip_code": "12345"},
            {"incorrect_field": "state", "message": ["Field may not be null."]}
        ),
        (
            {"name": "Test Venue", "street_address": "123 Main St.", "state": "NY", "city": None, "zip_code": "12345"},
            {"incorrect_field": "city", "message": ["Field may not be null."]}
        ),
        (
            {"name": "Test Venue", "street_address": "123 Main St.", "state": "NY", "city": "New York", "zip_code": None},
            {"incorrect_field": "zip_code", "message": ["Field may not be null."]}
        )
    ]
)
def test_create_new_venue_with_null_field_must_fail(flask_test_client, auth, user, json, test_input, expected):
    """Test that a new venue resource cannot be created
    if a field is None.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/venues",
        headers=get_headers(token),
        data=json.dumps(test_input)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"][expected["incorrect_field"]] == expected["message"]

    venue = Venue.query.first()
    assert venue is None


def test_create_new_venue_with_duplicate_address_must_fail(flask_test_client, auth, user, db, venue, json):
    """Test that a new venue with a duplicate street address
    cannot be created.
    """
    venue_object = {
        "name": "Test Jazz Club",
        "street_address": venue.street_address,
        "city": "New York",
        "state": "NY",
        "zip_code": "45677"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/venues",
        headers=get_headers(token),
        data=json.dumps(venue_object)
    )
    assert response.status == "409 CONFLICT"
    assert response.content_type == "application/json"
    assert response.json["message"] == "A venue with that street address already exists."

    #only the fixture should be in the database
    assert Venue.query.count() == 1

def test_update_venue_with_valid_data(flask_test_client, auth, user, db, venue, json):
    """Test that a venue resource can be succesfully updated
    when valid data is sent to the api.
    """
    venue_object = {
        "name": venue.name,
        "street_address": "678 Main St.",
        "city": venue.city,
        "state": venue.state,
        "zip_code": venue.zip_code
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/venues/{venue.id}",
        headers=get_headers(token),
        data=json.dumps(venue_object)
    )
    assert response.status == "204 NO CONTENT"
    assert response.content_type == "application/json"
    assert response.get_data(as_text=True) == ""

    updated_venue = Venue.query.filter_by(street_address=venue_object["street_address"]).first()
    assert updated_venue is not None
    assert updated_venue.name == venue.name
    assert updated_venue.street_address == venue_object["street_address"]
    assert updated_venue.city == venue.city
    assert updated_venue.state == venue.state
    assert updated_venue.zip_code == venue.zip_code


def test_update_venue_id_must_fail(flask_test_client, auth, user, json, venue):
    """Test that a venue's id cannot be updated."""
    updated_venue_object = {
        "id": 1000,
        "name": venue.name,
        "street_address": venue.street_address,
        "city": venue.city,
        "state": venue.state,
        "zip_code": venue.zip_code
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/venues/{venue.id}",
        headers=get_headers(token),
        data=json.dumps(updated_venue_object)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"]["id"] == ["Unknown field."]


def test_delete_venue(flask_test_client, auth, user, venue, db):
    """Test that a venue resource can be successfully deleted."""
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.delete(
        f"/api/v1/venues/{venue.id}",
        headers=get_headers(token)
    )
    assert response.status == "204 NO CONTENT"
    assert response.content_type == "application/json"
    assert response.get_data(as_text=True) == ""

    venue_object = Venue.query.get(venue.id)
    assert venue_object is None


def test_delete_venue_not_found_must_fail(flask_test_client, auth, user):
    """Test that a 404 error is returned if
    a venue with the given id does not
    exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.delete(
        "/api/v1/venues/100",
        headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Venue could not be found."
