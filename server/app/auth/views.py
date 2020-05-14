"""This module contains the view functions for authentication and
authorization.
"""


from http import HTTPStatus
from flask import Blueprint
from flask_restful import Api
from app.auth.resources import LoginAPI, RegisterAPI, LogoutAPI
from app.api.schemas import UserSchema


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")
api = Api(auth_blueprint)


api.add_resource(LoginAPI, "/login", endpoint="login")
api.add_resource(LogoutAPIm "/logout", endpoint="logout")
api.add_resource(
    RegisterAPI, "/register",
    resource_class_kwargs={"schema": UserSchema()},
    endpoint="register"
)


