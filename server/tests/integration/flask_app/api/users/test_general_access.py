"""This module contains tests for general access to the user endpoints."""


from pytest import mark
from flask_app.utils import get_headers


@mark.parametrize(
    "http_method, endpoint",
    [
        ("GET", "/api/v1/users"),
        ("GET", "/api/v1/users/1"),
        ("PUT", "/api/v1/users/1"),
        ("DELETE", "/api/v1/users/1")
    ]
)
def test_unauthorized_access(flask_test_client, http_method, endpoint):
    """Test to ensure that a 401 HTTP status is returned
    when the user routes are accessed
    without a token.
    """
    response = flask_test_client.open(
        method=http_method, path=endpoint, headers=get_headers()
    )
    assert response.status == "401 UNAUTHORIZED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Access token is invalid or expired."


@mark.parametrize(
    "http_method, endpoint",
    [
        ("POST", "/api/v1/users"),
        ("PUT", "/api/v1/users"),
        ("PATCH", "/api/v1/users"),
        ("DELETE", "/api/v1/users"),
        ("POST", "/api/v1/users/1"),
        ("PATCH", "/api/v1/users/1")
    ]
)
def test_http_method_not_allowed(flask_test_client, auth, user, http_method, endpoint):
    """Test to ensure that a 405 HTTP status is returned
    when an endpoint doesn't support a particular
    HTTP method.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.open(
        method=http_method, path=endpoint, headers=get_headers(token)
    )
    assert response.status == "405 METHOD NOT ALLOWED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "The method is not allowed for the requested URL."

