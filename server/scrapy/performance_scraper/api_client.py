"""This module contains a class that talks to the Flask API."""


import requests
import json
from performance_scraper.auth import AuthenticationClient


class FlaskAPIClient:
    """Class to send requests to the Flask API."""

    api_prefix = "/api/v1/"

    def __init__(self, token, auth_manager):
        self._token = token
        self._auth_manager = auth_manager

    def create_venue(self):
        pass

    def get_venue(self):
        pass

    def create_artist(self):
        pass

    def get_artist(self):
        pass

    def create_artist_image(self):
        pass

    def create_performance(self):
        pass

    def _get(self):
        pass

    def _post(self, item, endpoint, **kwargs):
        """Send a POST request containing from the given item to
        the given endpoint. Return the id of the newly created resource.
        """
        #get access token from access_token.json
        #if token is expired, call AuthenticationClient.login
        #if login is unsuccessful, call AuthenticationClient.register
        #Send actual request
        #if resource already exists, send GET request
        #return resource id
        pass

    def _put(self, item, endpoint, **kwargs):
        """Send a PUT request containing from the given item to
        the given endpoint.
        """
        #get access token from access_token.json
        #if token is expired, call AuthenticationClient.login
        #if login is unsuccessful, call AuthenticationClient.register
        #Send actual request
        #return nothing
        pass

    def _auth_headers(self):
        """Return auth headers necessary for making requests
        to the api.
        """
        if self._token is not None:
            headers = {"Authorization": f"Bearer {self._token}"}
        elif self._auth_manager:
            token = self._auth_manager.login()
            self._token = token
            headers = {"Authorization": f"Bearer {self._token}"}
        return headers

    def _internal_call(self):
        """Method for making calls to the API."""
        pass

