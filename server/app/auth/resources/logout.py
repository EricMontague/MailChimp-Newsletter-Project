"""This module contains the class-based view for logging out. REST apis
don't actually have a concept of logging out, but this view is necessary
for when the api is called from React to allow the user to log out.
"""


from flask_restul import Resource
from flask_jwt_extended import current_user, jwt_required
from app.auth.helpers import revoke_token
from flask_jwt_extended import get_raw_jwt
from http import HTTPStatus


class LogoutViewAPI(Resource):
    """View for logging a user out and revoking their token."""

    @jwt_required
    def post(self):
        """Log a user out and revoke their token."""
        token = get_raw_jwt()
        revoke_token(token)
        return {}, HTTPStatus.NO_CONTENT


