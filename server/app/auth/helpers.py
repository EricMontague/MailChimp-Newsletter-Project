"""This module contains various helper functions for performing common tasks
in the auth blueprint.
"""


from flask import current_app
from flask_jwt_extended import decode_token
from app.extensions import jwt
from app.models import User


@jwt.user_loader_callback_loader
def get_current_user(identity):
    """Callback function that takes the identity(sub) claim from a valid
    JWT and returns the currently authenticated user."""
    return User.query.get(identity)


def cache_token(token):
    """Store the given JWT in Redis."""
    decoded_token = decode_token(token)
    current_app.redis.hset(decoded_token["jti"], "revoked", "False")
    current_app.redis.expire(decoded_token["jti"], current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])


def revoke_token(token):
    """Revoke the given user's token."""
    decoded_token = decode_token(token)
    current_app.redis.hset(decoded_token["jti"], "revoked", "True")


@jwt.token_in_blacklist_loader
def is_blacklisted(decoded_token):
    """Return True if the token provided by the
    client is blacklisted.
    """
    is_revoked = current_app.redis.hget(decoded_token["jti"], "revoked")
    if is_revoked is None or is_revoked == "True":
        return True
    return False

