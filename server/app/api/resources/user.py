"""This module contains the user resources"""


from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.models import User
from app.extensions import db
from http import HTTPStatus


#these classes will be used later when I add a front end to this project
class UserAPI(Resource):
    """Class to represent a single user resource."""
    
    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self, user_id):
        """Return a single user resource."""
        user = User.query.get(user_id)
        if user is None:
            return {"message": "User could not be found"}, HTTPStatus.NOT_FOUND
        return self._schema.dump(user), HTTPStatus.OK

    def put(self, user_id):
        """Update a single user resource."""
        json_data = request.get_json()
        try:
            updated_user = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.message}, HTTPStatus.BAD_REQUEST
        user = User.query.get(user_id)
        if user is None:
            return {"message": "User could not be found"}, HTTPStatus.NOT_FOUND
        user.username = updated_user.username
        user.email = updated_user.email
        user.password_hash = updated_user.password_hash
        db.session.commit()
        return self._schema.dump(user), HTTPStatus.NO_CONTENT

    def delete(self, user_id):
        """Delete a single user resource."""
        user = User.query.get(user_id)
        if user is None:
            return {"message": "User could not be found"}, HTTPStatus.NOT_FOUND
        db.session.delete(user)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT


class UserListAPI(Resource):
    """Class to represent a collection of user resources."""
    
    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self):
        """Return all user resources."""
        users = User.query.all()
        return self._schema.dump(users, many=True), HTTPStatus.OK        
    