"""This module is for testing the registration route."""


from pytest import mark
from flask_app.utils import generate_user_instance


def test_register_with_valid_input(flask_test_client, json):
    """Test that registration is successful with valid input."""
    user_object = {
        "username": "test_user", "password": "password", "email": "test@gmail.com"
    }
    response = flask_test_client.post(
        "/auth/register",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        data=json.dumps(user_object)
    )
    assert response.status == "201 CREATED"
    json_response = json.loads(response.get_data(as_text=True))
    assert json_response["access_token"] is not None
    
    
@mark.parametrize(
    "test_input, expected",
    [   
        (
            {"password": "password", "email": "test@gmail.com"}, 
            {"incorrect_field": "username", "message": ["Missing data for required field."]}
        ),
        (
            {"username": "test", "password": None, "email": "fudge"},
            {"incorrect_field": "password", "message": ["Field may not be null."]}
        ),
        (
            {"username": "", "password": "password", "email": "test@gmail.com"},
            {"incorrect_field": "username", "message": ["Length must be between 1 and 64."]}
        ),
        (
            {"username": "test" * 100, "password": "password", "email": "test@gmail.com"},
            {"incorrect_field": "username", "message": ["Length must be between 1 and 64."]}
        ),
        (
            {"username": "test", "password": "pass", "email": "test@gmail.com"},
            {"incorrect_field": "password", "message": ["Length must be between 8 and 30."]}
        ),
        (
            {"username": "test", "password": "password", "email": "fudge"},
            {"incorrect_field": "email", "message": ["Not a valid email address."]}
        )
    ]
)
def test_register_with_invalid_input(flask_test_client, json, test_input, expected):
    """Test that the approriate error messages and HTTP status codes
    are returned when invalid data is sent to the registration route.
    """
    response = flask_test_client.post(
        "/auth/register",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        data=json.dumps(test_input)
    )
    assert response.status == "400 BAD REQUEST"
    json_response = json.loads(response.get_data(as_text=True))
    assert json_response["message"][expected["incorrect_field"]] == expected["message"]
    assert json_response.get("access_token", None) is None


def test_register_user_already_exists(flask_test_client, db, json, user):
    """Test to ensure that a new user resource isn't created if one already exists."""
    db.session.add(user)
    db.session.commit()
    duplicate_user = {
        "username": user.username, 
        "password": "password", 
        "email": user.email
    }
    response = flask_test_client.post(
        "/auth/register",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        data=json.dumps(duplicate_user)
    )
    assert response.status == "409 CONFLICT"
    json_response = json.loads(response.get_data(as_text=True))
    assert json_response["message"] == "User already registered."
    assert json_response.get("access_token", None) is None
