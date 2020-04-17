"""This module contains a class that is used to authenticate
with the flask API.
"""


import os
import requests
import json
from scrapy.conf import settings


class AuthManager:
    """Class to authenticate with the Flask API."""

    api_prefix = "/api/v1/"

    def __init__(self, username, password, email):
        self._username = username
        self._password = password
        self._email = email
    
    def login(self):
        """Send a POST request to the login endpoint of the API.
        Upon a successful login, store the returned JWT
        in a file for future requests.
        """
        pass

    def is_token_expired(self, token):
        """Return True if the given token is expired."""
        expired_date = token["exp"]

    def _register(self):
        """Send a POST request to the register endpoint of the API.
        Upon a successful registration, store the returned JWT
        in a file for future requests.
        """
        pass

    def _get_headers(self):
        """Return headers necessary for making a call to the API."""
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        return headers

    def _store_token(self, data):
        """Store the given dictionary containing a JWT in a file."""
        token_file_path = settings.get("TOKEN_FILE_PATH")
        with open(token_file_path, "w") as token_file:
            json.dump(data, token_file)
    
    @staticmethod
    def retrieve_token():
        """Return token stored in a file."""
        token_file_path = settings.get("TOKEN_FILE_PATH")
        with open(token_file_path, "r") as token_file:
            data = json.load(token_file)
        return data["access_token"]

