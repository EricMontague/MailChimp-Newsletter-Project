"""This module contains integration tests for the user model."""


from pytest import raises
from app.models import User


def test_setting_password():
    """Test that when the password is set,
    a password hash is generated.
    """
    user = User(
        username="firstuser",
        password="password",
        email="firstuser@gmail.com"
    )
    assert user.password_hash is not None
    

def test_password_verification_successful(user):
    """Test user password verification when the correct
    password is given.
    """
    assert user.verify_password("password") is True
    

def test_password_verification_unsuccessful(user):
    """Test user password verification when the incorrect
    password is given.
    """
    assert user.verify_password("pass") is False


def test_password_salts_are_random():
    """Test that the same password generates two different
    password hashes for two different users.
    """
    first_user = User(
        username="firstuser",
        password="password",
        email="firstuser@gmail.com"
    )
    second_user = User(
        username="otheruser",
        password="password",
        email="seconduser@gmail.com"
    )
    assert first_user.password_hash != second_user.password_hash
