"""This module contains tests for sending GET requests to the venue endpoints."""


from pytest import mark
from flask_app.utils import get_headers


def test_getting_single_venue_by_authorized_user(flask_test_client, venue, auth, user):
    """Test to ensure that a single venue resource can be
    successfully retrieved by an authorized user
    """
    expected_fields = {
        "id", "name", "street_address", "city", "state", "zip_code", "performances", "_links"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/venues/{venue.id}",
        headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == expected_fields
    assert response.json["id"] == venue.id
    assert response.json["name"] == venue.name
    assert response.json["street_address"] == venue.street_address
    assert response.json["city"] == venue.city
    assert response.json["state"] == venue.state
    assert response.json["zip_code"] == venue.zip_code
    assert response.json["_links"]["uri"] == f"/api/v1/venues/{venue.id}"
    assert response.json["_links"]["collection"] == "/api/v1/venues"


def test_getting_single_venue_by_name(flask_test_client, venue, auth, user):
    """Test to ensure that a venue can be retrieved by name."""
    expected_fields = {
        "id", "name", "street_address", "city", "state", "zip_code", "performances", "_links"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/venues/{venue.name}",
        headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == expected_fields
    assert response.json["id"] == venue.id
    assert response.json["name"] == venue.name
    assert response.json["street_address"] == venue.street_address
    assert response.json["city"] == venue.city
    assert response.json["state"] == venue.state
    assert response.json["zip_code"] == venue.zip_code
    assert response.json["_links"]["uri"] == f"/api/v1/venues/{venue.id}"
    assert response.json["_links"]["collection"] == "/api/v1/venues"


def test_getting_single_venue_with_incorrect_name_must_fail(flask_test_client, auth, user, venue):
    """Test to ensure that a 404 status is returned if a venue of a
    particular name doesn't exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/venues/venue_not_found",
        headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Venue could not be found."
    
def test_getting_single_venue_without_token_must_fail(flask_test_client, venue):
    """Test to ensure that an unauthorized  user (no token) cannot get
    a venue resource.
    """
    response = flask_test_client.get(
        f"/api/v1/venues/{venue.id}",
        headers=get_headers()
    )
    assert response.status == "401 UNAUTHORIZED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Access token is invalid or expired."


def test_getting_list_of_venues_by_authorized_user(flask_test_client, json, auth, venue, user):
    """Test to ensure that a list of venue resources can be
    successfully retrieved.
    """
    expected_fields = {
        "id", "name", "street_address", "city", "state", "zip_code", "performances", "_links"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/venues",
        headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == {"venues", "prev", "next", "total"}
    assert isinstance(json.loads(response.json["venues"]), list)
    assert set(json.loads(response.json["venues"])[0].keys()) == expected_fields
    assert response.json["total"] == 1
    assert response.json["prev"] is None
    assert response.json["next"] is None
    assert json.loads(response.json["venues"])[0]["id"] == venue.id
    assert json.loads(response.json["venues"])[0]["name"] == venue.name
    assert json.loads(response.json["venues"])[0]["street_address"] == venue.street_address
    assert json.loads(response.json["venues"])[0]["city"] == venue.city
    assert json.loads(response.json["venues"])[0]["state"] == venue.state
    assert json.loads(response.json["venues"])[0]["zip_code"] == venue.zip_code
    assert json.loads(response.json["venues"])[0]["performances"] == venue.performances.all()
    assert json.loads(response.json["venues"])[0]["_links"]["uri"] == f"/api/v1/venues/{venue.id}"    
    assert json.loads(response.json["venues"])[0]["_links"]["collection"] == "/api/v1/venues"


def test_getting_list_of_venues_without_token_must_fail(flask_test_client):
    """Test to ensure that an unauthorized user (no token) cannot get
    venue resources
    """
    response = flask_test_client.get(
        "/api/v1/venues",
        headers=get_headers()
    )
    assert response.status == "401 UNAUTHORIZED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Access token is invalid or expired."


def test_venue_not_found(flask_test_client, auth, user):
    """Test to ensure that a 404 response is returned
    if a venue resource does not exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        "/api/v1/venues/100",
        headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Venue could not be found."
    