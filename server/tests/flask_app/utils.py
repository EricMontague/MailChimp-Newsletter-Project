"""This module contains helper functions for testing."""

import json


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def register(self, username="test", password="password", email="test@gmail.com"):
        response = self._client.post(
            "/auth/register",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            data=json.dumps({"username": username, "password": password, "email": email})
        )
        return response.json["access_token"]

  
def generate_user_instance(username="username", password="password", email="user@gmail.com"):
    """Return an instance of a User for testing."""
    from app.models import User
    return User(username=username, password=password, email=email)


def get_headers(token=None):
    """Return headers necessary for making requests
    to the api.
    """
    if token is not None:
        headers = {
            "Content-Type": "application/json", 
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
    else:
        headers={
            "Content-Type": "application/json", 
            "Accept": "application/json"
        }
    return headers
