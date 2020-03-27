"""This module is for testing the login route."""


from pytest import mark


@mark.parametrize(
    "test_input, expected",
    [
        (
            {"username": "test", "password": "password"},
            {"status": "201 CREATED"}
        )
    ]
)
def test_login_valid_input(flask_test_client, auth, json, test_input, expected):
    """Test that the login route returns an access token
    when a valid username and password is sent.
    """
    #register method returns a dictionary that contains the access token, but
    #it isn't needed for this test
    auth.register(username="test", password="password", email="test@gmail.com")
    response = flask_test_client.post(
        "/auth/login",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        data=json.dumps(test_input)
    )
    assert response.status == expected["status"]
    json_response = json.loads(response.get_data(as_text=True))
    assert json_response["access_token"] is not None


@mark.parametrize(
    "test_input, expected",
    [
        (
            {"password": "password"},
            {"status": "401 UNAUTHORIZED", "message": "Missing username or password."}
        ),
        (
            {"username": "test"},
            {"status": "401 UNAUTHORIZED", "message": "Missing username or password."}
        ),
        (
            {},
            {"status": "401 UNAUTHORIZED", "message": "Missing username or password."}
        ),
        (
            {"username": "bad_username", "password": "password"},
            {"status": "401 UNAUTHORIZED", "message": "Bad credentials."}
        ),
        (
            {"username": "test", "password": "bad_password"},
            {"status": "401 UNAUTHORIZED", "message": "Bad credentials."}
        )
    ]
)
def test_login_invalid_input(flask_test_client, auth, json, test_input, expected):
    """Test that the approriate error messages and HTTP status codes
    are returned when invalid data is sent to the login route.
    """
    #register method returns a dictionary that contains the access token, but
    #it isn't needed for this test
    auth.register(username="test", password="password", email="test@gmail.com")
    response = flask_test_client.post(
        "/auth/login",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        data=json.dumps(test_input)
    )
    assert response.status == expected["status"]
    json_response = json.loads(response.get_data(as_text=True))
    assert json_response["message"] == expected["message"]
    assert json_response.get("access_token", None) is None

