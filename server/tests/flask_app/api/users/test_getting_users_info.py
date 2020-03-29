"""This module contains tests for sending GET requests to the user endpoints."""


from pytest import mark
from flask_app.utils import get_headers


def test_getting_single_user_by_authorized_user(flask_test_client, auth, user):
    """Test to ensure that a single user resource can be
    successfully retrieved.
    """
    expected_fields = {"id", "username", "email", "_links"}
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/users/{user.id}",
        headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == expected_fields
    assert response.json["id"] == user.id
    assert response.json["username"] == user.username
    assert response.json["email"] == user.email
    assert response.json.get("password") is None
    assert response.json["_links"]["uri"] == f"/api/v1/users/{user.id}"
    assert response.json["_links"]["collection"] == "/api/v1/users"


def test_getting_single_user_without_token_must_fail(flask_test_client, user):
    """Test to ensure that an unauthorized  user (no token) cannot get
    a user resource.
    """
    response = flask_test_client.get(
        f"/api/v1/users/{user.id}",
        headers=get_headers() #no token sent
    )
    assert response.status == "401 UNAUTHORIZED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Access token is invalid or expired."


def test_getting_list_of_users_by_authorized_user(flask_test_client, json, auth, user):
    """Test to ensure that a list of user resources can be
    successfully retrieved.
    """
    expected_fields = {"users", "prev", "next", "total"}
    expected_user_fields = {"id", "username", "email", "_links"}
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/users",
        headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == expected_fields
    assert isinstance(json.loads(response.json["users"]), list)
    assert set(json.loads(response.json["users"])[0].keys()) == expected_user_fields
    assert response.json["total"] == 1
    assert response.json["prev"] is None
    assert response.json["next"] is None
    assert json.loads(response.json["users"])[0]["id"] == user.id
    assert json.loads(response.json["users"])[0]["username"] == user.username
    assert json.loads(response.json["users"])[0]["email"] == user.email
    assert json.loads(response.json["users"])[0].get("password") is None
    assert json.loads(response.json["users"])[0]["_links"]["uri"] == f"/api/v1/users/{user.id}"    
    assert json.loads(response.json["users"])[0]["_links"]["collection"] == "/api/v1/users"


def test_getting_list_of_users_without_token_must_fail(flask_test_client):
    """Test to ensure that an unauthorized user (no token) cannot get
    user resources
    """
    response = flask_test_client.get(
        f"/api/v1/users",
        headers=get_headers() #no token
    )
    assert response.status == "401 UNAUTHORIZED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Access token is invalid or expired."


def test_user_not_found(flask_test_client, auth, user):
    """Test to ensure that a 404 response is returned
    if a user resource does not exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/users/100",
        headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "User could not be found."
