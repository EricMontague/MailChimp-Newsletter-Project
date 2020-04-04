"""This module contains unit tests for the user model."""


from pytest import raises
from app.models import User
from unittest.mock import patch


@patch("app.models.user.generate_password_hash")
def test_setting_password(generate_password_mock):
    """Test that when the password is set,
    a password hash is generated.
    """
    generate_password_mock.return_value = "wgion9402trgjw"
    user = User(
        username="firstuser",
        password="password",
        email="firstuser@gmail.com"
    )
    assert user.password_hash is not None
    assert user.password_hash == "wgion9402trgjw"


@patch("app.models.user.check_password_hash")
def test_password_verification_successful(check_password_mock, user):
    """Test user password verification when the correct
    password is given.
    """
    check_password_mock.return_value = True
    assert user.verify_password("password") is True


@patch("app.models.user.check_password_hash")
def test_password_verification_successful(check_password_mock, user):
    """Test user password verification when the incorrect
    password is given.
    """
    check_password_mock.return_value = False
    assert user.verify_password("password") is False


def test_no_password_getter(user):
    """Test that the password attribute is not readable."""
    with raises(AttributeError):
        user.password


def test_repr(user):
    """Test that the __repr__ method returns
    the expected value.
    """
    assert user.__repr__() == f"<User: '{user.username}'>"

