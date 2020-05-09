"""This module contains a class that is used to authenticate
with the flask API.
"""


import requests
import json
from http import HTTPStatus
from scrapy.utils.project import get_project_settings
from app.performance_scraper.performance_scraper.flask_api.exceptions import FlaskAPIException


class AuthManager:
    """Class to authenticate with the Flask API."""

    api_prefix = "http://127.0.0.1:5000/auth/"

    def __init__(self, username, password, email, cache_path):
        self.username = username
        self.password = password
        self.email = email
        self.cache_path = cache_path
    
    def login(self):
        """Send a POST request to the login endpoint of the API.
        Upon a successful login, store the returned JWT
        in a file for future requests. Afterwards, return
        the JWT that was sent from the API.
        """
        payload = {"username": self.username, "password": self.password}
        try:
            response = requests.post(
                self.api_prefix + "login",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            token = response.json()["access_token"]
        except requests.exceptions.HTTPError:
            if response.status_code == HTTPStatus.UNAUTHORIZED:
                token = self._register()
            else:
                try:
                    message = response.json()["message"]
                except (ValueError, KeyError):
                    message = "An error occurred."
                    raise FlaskAPIException(
                        response.status_code,
                        f"{response.url}:\n {message}"
                    )
        self._store_token(token)
        return token

    def _register(self):
        """Send a POST request to the register endpoint of the API.
        Upon a successful registration, return the JWT sent by the API.
        """
        payload = {"username": self.username, "password": self.password, "email": self.email}
        try:
            response = requests.post(
                self.api_prefix + "register",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            token = response.json()["access_token"]
        except requests.exceptions.HTTPError:
            #attempt to retrieve error message
            try:
                message = response.json()["message"]
            except (ValueError, KeyError):
                message = "An error occurred."
            raise FlaskAPIException(
                response.status_code,
                f"{response.url}:\n {message}"
            )
        return token

    def _get_headers(self):
        """Return headers necessary for making a call to the API."""
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        return headers

    def _store_token(self, data):
        """Store the given dictionary containing a JWT in a file."""
        with open(self.cache_path, "w") as token_file:
            json.dump(data, token_file)
    
    def get_cached_token(self):
        """Return token stored in a file."""
        with open(self.cache_path, "r") as token_file:
            data = json.load(token_file)
        return data

