"""This module contains the class for the login endpoint."""


from http import HTTPStatus
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from app.models import User


class LoginAPI(Resource):
    """Class to represent the login endpoint."""

    def post(self):
        """Authenticate user and return a JWT to the client."""
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if username is None or password is None:
            return {"message": "Missing username or password."}, HTTPStatus.UNAUTHORIZED
            
        #verify username and password
        user = User.query.filter_by(username=username).first()
        if user is None or not user.verify_password(password):
            return {"message": "Bad credentials."}, HTTPStatus.UNAUTHORIZED
        
        #create access and refresh tokens
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, HTTPStatus.CREATED
        