"""This module contains the class for the registrtation endpoint."""


from http import HTTPStatus
from flask import request, jsonify
from flask_restful import Resource
from app.extensions import db
from app.models import User
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token


class RegisterAPI(Resource):
    """Class to represent the registration endpoint."""

    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def post(self):
        """Create a new user account and return a JWT to the client."""
        json_data = request.get_json()
        try:
            new_user = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.messages}, HTTPStatus.BAD_REQUEST
        #check for an existing user
        existing_user = User.query.get(new_user.id)
        if existing_user is not None:
            return {"message": "User already registered"}, HTTPStatus.ACCEPTED
        db.session.add(new_user)
        db.session.commit()

        #create acesss token
        access_token = create_access_token(identity=new_user.id)
        return jsonify({"access_token": access_token}), HTTPStatus.CREATED
