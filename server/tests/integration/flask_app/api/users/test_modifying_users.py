"""This module contains tests for modifying user resources."""


from pytest import mark
from flask_app.utils import get_headers
from app.models import User


def test_update_user_info_with_valid_data(flask_test_client, auth, db, user, json):
    """Test that a user resource can be succesfully updated
    when valid data is sent to the api.
    """
    updated_user_object = {
        "username": user.username,
        "password": "password",
        "email": "new_email@gmail.com"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/users/{user.id}",
        headers=get_headers(token),
        data=json.dumps(updated_user_object)
    )
    assert response.status == "204 NO CONTENT"
    assert response.content_type == "application/json"
    assert response.get_data(as_text=True) == ""

    updated_user = User.query.get(user.id)
    assert updated_user is not None
    assert updated_user.username == user.username
    assert updated_user.email == updated_user_object["email"]
    

#may end up putting these in a separate module
@mark.parametrize(
    "test_input, expected",
    [
        (
            {"username": "testing", "password": "password"},
            {"incorrect_field": "email", "message": ["Missing data for required field."]}
        ),
        (
            {"password": "password", "email": "testing@gmail.com"},
            {"incorrect_field": "username", "message": ["Missing data for required field."]}
        ),
        (
            {"username": "testing", "email": "testing@gmail.com"},
            {"incorrect_field": "password", "message": ["Missing data for required field."]}
        ),
        (
            {"username": "testing", "password": "password", "email": "testing.com"},
            {"incorrect_field": "email", "message": ["Not a valid email address."]}
        ),
        (
            {"username": "testing" * 10, "password": "password", "email": "testing@gmail.com"},
            {"incorrect_field": "username", "message": ["Length must be between 1 and 64."]}
        ),
        (
            {"username": "testing", "password": "pass", "email": "testing@gmail.com"},
            {"incorrect_field": "password", "message": ["Length must be between 8 and 30."]}
        ),
        (
            {"username": "", "password": "password", "email": "testing@gmail.com"},
            {"incorrect_field": "username", "message": ["Length must be between 1 and 64."]}
        ),
        (
            {"username": "testing", "password": None, "email": "testing@gmail.com"},
            {"incorrect_field": "password", "message": ["Field may not be null."]}
        )
    ]
)
def test_update_user_info_with_invalid_data_must_fail(flask_test_client, auth, 
                                                        db, json, test_input, 
                                                        user, expected):
    """Test that a user resource cannot be updated
    if invalid data is passed to the api.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/users/{user.id}",
        headers=get_headers(token),
        data=json.dumps(test_input)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"][expected["incorrect_field"]] == expected["message"]

    if test_input.get("username") is not None:
        updated_user = User.query.filter_by(username=test_input["username"]).first()
        assert updated_user is None


def test_update_user_id_must_fail(flask_test_client, auth, json, user):
    """Test that a user's id cannot be updated."""
    updated_user_object = {
        "id": 1000,
        "username": user.username,
        "password": "password",
        "email": user.email
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/users/{user.id}",
        headers=get_headers(token),
        data=json.dumps(updated_user_object)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"]["id"] == ["Unknown field."]


def test_delete_user(flask_test_client, auth, user, db):
    """Test that a user resource can be successfully deleted."""
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.delete(
        f"/api/v1/users/{user.id}",
        headers=get_headers(token)
    )
    assert response.status == "204 NO CONTENT"
    assert response.content_type == "application/json"
    assert response.get_data(as_text=True) == ""

    user = User.query.get(user.id)
    assert user is None


def test_delete_user_not_found_must_fail(flask_test_client, auth, user):
    """Test that a 404 error is returned if
    a user with the given id does not
    exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.delete(
        "/api/v1/users/100",
        headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "User could not be found."
