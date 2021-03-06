"""This module contains tests for sending GET requests to the artist endpoints."""


from pytest import mark
from flask_app.utils import get_headers


def test_getting_single_artist_by_authorized_user(flask_test_client, auth, user, artist):
    """Test to ensure that a single artist resource can be
    successfully retrieved.
    """
    expected_fields = {
        "id", "name", "bio", "website", "performances", "image", "_links"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/artists/{artist.id}",
        headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == expected_fields
    assert response.json["id"] == artist.id
    assert response.json["name"] == artist.name
    assert response.json["bio"] == artist.bio
    assert response.json["website"] == artist.website
    assert response.json["performances"] == []
    assert response.json["image"] is None
    assert response.json["_links"]["uri"] == f"/api/v1/artists/{artist.id}"
    assert response.json["_links"]["collection"] == "/api/v1/artists"


def test_getting_single_artist_without_token_must_fail(flask_test_client, artist):
    """Test to ensure that an unauthorized  user (no token) cannot get
    an artist resource.
    """
    response = flask_test_client.get(
        f"/api/v1/artists/{artist.id}",
        headers=get_headers() #no token sent
    )
    assert response.status == "401 UNAUTHORIZED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Access token is invalid or expired."


def test_getting_single_artist_by_name(flask_test_client, artist, auth, user):
    """Test to ensure that an artist can be retrieved by name."""
    expected_fields = {
        "id", "name", "bio", "website", "performances", "image", "_links"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/artists/{artist.name}",
        headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == expected_fields
    assert response.json["id"] == artist.id
    assert response.json["name"] == artist.name
    assert response.json["bio"] == artist.bio
    assert response.json["website"] == artist.website
    assert response.json["performances"] == []
    assert response.json["image"] is None
    assert response.json["_links"]["uri"] == f"/api/v1/artists/{artist.id}"
    assert response.json["_links"]["collection"] == "/api/v1/artists"

def test_getting_single_artist_with_incorrect_name_must_fail(flask_test_client, auth, user, artist):
    """Test to ensure that a 404 status is returned if an artist of a
    particular name doesn't exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/artists/artist_not_found",
        headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Artist could not be found."

def test_getting_list_of_artists_by_authorized_user(flask_test_client, json, auth, user, artist):
    """Test to ensure that a list of artist resources can be
    successfully retrieved.
    """
    expected_fields = {
        "id", "name", "bio", "website", "performances", "image", "_links"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/artists",
        headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == {"artists", "prev", "next", "total"}
    assert isinstance(json.loads(response.json["artists"]), list)
    assert set(json.loads(response.json["artists"])[0].keys()) == expected_fields
    assert response.json["total"] == 1
    assert response.json["prev"] is None
    assert response.json["next"] is None
    assert json.loads(response.json["artists"])[0]["id"] == artist.id
    assert json.loads(response.json["artists"])[0]["name"] == artist.name
    assert json.loads(response.json["artists"])[0]["bio"] == artist.bio
    assert json.loads(response.json["artists"])[0]["website"] == artist.website
    assert json.loads(response.json["artists"])[0]["performances"] == []
    assert json.loads(response.json["artists"])[0]["image"] is None
    assert json.loads(response.json["artists"])[0]["_links"]["uri"] == f"/api/v1/artists/{artist.id}"    
    assert json.loads(response.json["artists"])[0]["_links"]["collection"] == "/api/v1/artists"


def test_getting_list_of_artists_without_token_must_fail(flask_test_client):
    """Test to ensure that an unauthorized user (no token) cannot get
    artist resources
    """
    response = flask_test_client.get(
        f"/api/v1/artists",
        headers=get_headers() #no token
    )
    assert response.status == "401 UNAUTHORIZED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Access token is invalid or expired."


def test_artist_not_found(flask_test_client, auth, user):
    """Test to ensure that a 404 response is returned
    if an artist resource does not exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/artists/100",
        headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Artist could not be found."
