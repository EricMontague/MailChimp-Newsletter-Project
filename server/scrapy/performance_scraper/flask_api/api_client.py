"""This module contains a class that talks to the Flask API."""


import requests
import json
from performance_scraper.flask_api.exceptions import FlaskAPIException


class FlaskAPIClient:
    """Class to send requests to the Flask API."""

    api_prefix = "http://127.0.0.1:5000/api/v1/"

    def __init__(self, token=None, auth_manager=None):
        self._token = token
        self.auth_manager = auth_manager

    def create_venue(self, payload):
        """Send a POST request to the API to create a venue resource.
        Returns the newly created resource.
        """
        return self._internal_call("POST", "venues", payload=payload)

    def get_venue_by_name(self, name):
        """Send a GET request to the API to retrieve a venue by name."""
        return self._internal_call("GET", f"venues/{name}")

    def create_artist(self, payload):
        """Send a POST request to the API to create an artist resource.
        Returns the newly created resource.
        """
        return self._internal_call("POST", "artists", payload=payload)

    def get_artist_by_name(self, name):
        """Send a GET request to the API to retrieve an artist by name."""
        return self._internal_call("GET", f"artists/{name}")

    def update_artist_image(self, artist_id, payload):
        """Send a PUT request to the API to replace an artist's image. If an image 
        doesn't exist, then one is created. Returns None.
        """
        return self._internal_call("PUT", f"artists/{artist_id}/images", payload=payload)

    def create_performance(self, payload):
        """Send a POST request to the API to create a performance resource.
        Returns the newly created resource.
        """
        return self._internal_call("POST", "performances", payload=payload)

    def _get_headers(self):
        """Return the headers necessary for making requests
        to the api.
        """
        if self._token is not None:
            headers = {"Authorization": f"Bearer {self._token}"}
        elif self.auth_manager is not None:
            self._token = self.auth_manager.login()
            headers = {"Authorization": f"Bearer {self._token}"}
        else:
            headers = {}
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        return headers

    def _internal_call(self, method, url, payload=None, query_string_parameters=None):
        """Method for making calls to the API."""
        data = {}
        headers = self._get_headers()
        if payload is not None:
            data = json.dumps(payload)
        try:
            response = requests.request(
                method,
                self.api_prefix + url,
                headers=headers,
                params=query_string_parameters,
                **data,
            )
            response.raise_for_status()
            json_response = response.json()
        except requests.exceptions.HTTPError:
            # attempt to retrieve error message
            try:
                message = response.json()["message"]
            except (ValueError, KeyError):
                message = "An error occurred during your request. No error message could be found."
            raise FlaskAPIException(
                response.status_code, f"{response.url}:\n {message}"
            )
        except ValueError:  # a put request will not return a JSON response
            json_response = None
        return json_response

