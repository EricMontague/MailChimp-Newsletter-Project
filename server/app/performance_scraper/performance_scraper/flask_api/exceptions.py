"""This module contains custom exception classes for the Flask API."""


class FlaskAPIException(Exception):
    """Class to represent an exception raised by the Flask API."""

    def __init__(self, http_status, message):
        self.http_status = http_status
        self.message = message

    def __str__(self):
        """Return a string representation of the raised exception."""
        return f"HTTP Status: {self.http_status} - {self.message}"
        