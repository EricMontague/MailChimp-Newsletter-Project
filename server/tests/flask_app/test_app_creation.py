"""This module is for testing that the application instance is
successfully created and configured properly.
"""


import pytest
from app import create_app


@pytest.mark.parametrize("config_name", ["production", "development", "testing"])
def test_create_app_passing_config_name(config_name):
    """Test to ensure the successfully creation of the application
    instance.
    """
    assert create_app(config_name) is not None


def test_create_app_with_non_existing_config():
    """Test to ensure the application factory function
    throws an error when an incorrect configuration name
    is passed in.
    """
    with pytest.raises(KeyError):
        create_app("wrong_config_name")

