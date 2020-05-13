"""This module contains various helper functions for performing common tasks
in the auth blueprint.
"""


from app.extensions import jwt
from app.models import User


@jwt.user_loader_callback_loader
def get_current_user(identity):
    """Callback function that takes the identity(sub) claim from a valid
    JWT and returns the currently authenticated user."""
    return User.query.get(identity)

