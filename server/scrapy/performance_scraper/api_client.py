"""This module contains a class that talks to the Flask API."""


import requests
import json


class FlaskAPIClient:
    """Class to send requests to the Flask API."""

    api_prefix = "/api/v1/"

    def __init__(self, token=None, auth_manager=None):
        self._token = token
        self.auth_manager = auth_manager

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

    def _get_headers(self):
        """Return the headers necessary for making requests
        to the api.
        """
        if self._token is not None:
            headers = {"Authorization": f"Bearer {self._token}"}
        elif self.auth_manager is not None:
            token = self.auth_manager.login()
            self._token = token
            headers = {"Authorization": f"Bearer {self._token}"}
        else:
            headers = {}
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        return headers

    def _internal_call(self, method, url, payload=None):
        """Method for making calls to the API."""
        kwargs = {}
        headers = self._get_headers()
        if payload is not None:
            kwargs = json.dumps(payload)
        try:
            response = requests.request(
                method,
                self.api_prefix + url,
                headers=headers,
                **kwargs
            )
            response.raise_for_status()
            json_response = response.json()
        except requests.exceptions.HTTPError:
            #attempt to retrieve error message
            try:
                message = response.json()["message"]
            except (ValueError, KeyError):
                message = "An error occurred."
            #logging needed here
            raise FlaskAPIException
        except ValueError: #a put request will not return a JSON response
            json_response = None
        return json_response
        

