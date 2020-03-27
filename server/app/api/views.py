"""This module contains all of the endpoints for the api."""


from http import HTTPStatus
from flask import Blueprint, jsonify
from flask_restful import Api
from flask_jwt_extended import verify_jwt_in_request
from .resources import (
    ArtistAPI,
    ArtistListAPI,
    VenueAPI,
    VenueListAPI,
    ImageAPI,
    ImageListAPI,
    PerformanceAPI,
    PerformanceListAPI,
    UserAPI,
    UserListAPI
)
from .schemas import (
    ArtistSchema,
    VenueSchema,
    ImageSchema,
    PerformanceSchema,
    UserSchema
)

#Instantiate Blueprint and Api objects
api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_blueprint)


@api_blueprint.before_request
def before_request():
    """Ensure that a user has a valid access token before each
    request in this blueprint.
    """
    try:
        verify_jwt_in_request()
    except:
        return jsonify({"message": "Access token is invalid or expired."}), HTTPStatus.UNAUTHORIZED


#artist resources
api.add_resource(
    ArtistListAPI, 
    "/artists", 
    resource_class_kwargs={"schema": ArtistSchema()},
    endpoint="artist_list"
)
api.add_resource(
    ArtistAPI, 
    "/artists/<int:artist_id>",
    resource_class_kwargs={"schema": ArtistSchema()},
    endpoint="artist"
)


#image resources
api.add_resource(
    ImageListAPI,
    "/images",
    resource_class_kwargs={"schema": ImageSchema()},
    endpoint="image_list"
)
api.add_resource(
    ImageAPI,
    "/images/<int:image_id>",
    resource_class_kwargs={"schema": ImageSchema()},
    endpoint="image"
)


#performance resources
api.add_resource(
    PerformanceListAPI,
    "/performances",
    resource_class_kwargs={"schema": PerformanceSchema()},
    endpoint="performance_list"
)
api.add_resource(
    PerformanceAPI,
    "/performances/<int:performance_id>",
    resource_class_kwargs={"schema": PerformanceSchema()},
    endpoint="performance"
)


#user resources
api.add_resource(
    UserListAPI,
    "/users",
    resource_class_kwargs={"schema": UserSchema()},
    endpoint="user_list"
)
api.add_resource(
    UserAPI,
    "/users/<int:user_id>",
    resource_class_kwargs={"schema": UserSchema()},
    endpoint="user"
)


#venue resources
api.add_resource(
    VenueListAPI,
    "/venues",
    resource_class_kwargs={"schema": VenueSchema()},
    endpoint="venue_list"
)
api.add_resource(
    VenueAPI,
    "/venues/<int:venue_id>",
    resource_class_kwargs={"schema": VenueSchema()},
    endpoint="venue"
)
