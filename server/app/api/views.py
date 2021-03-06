"""This module contains all of the endpoints for the api."""


from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_restful import Api
from flask_jwt_extended import verify_jwt_in_request
from app.api.resources import (
    ArtistAPI,
    ArtistListAPI,
    ArtistByNameAPI,
    VenueAPI,
    VenueByNameAPI,
    VenueListAPI,
    ArtistImageListAPI,
    PerformanceAPI,
    PerformanceListAPI,
    ArtistPerformanceListAPI,
    UserAPI,
    UserListAPI,
    CrawlTaskAPI,
    CrawlTaskStatusAPI,
    CrawlGroupAPI
)
from app.api.schemas import (
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
    """Before request hook for the api."""
    try:
        verify_jwt_in_request()
    except:
        return jsonify({"message": "Access token is invalid or expired."}), HTTPStatus.UNAUTHORIZED
    

#artist resources
api.add_resource(
    ArtistListAPI, 
    "/artists", 
    resource_class_kwargs={"schema": ArtistSchema()},
    endpoint="artists"
)
api.add_resource(
    ArtistAPI, 
    "/artists/<int:artist_id>",
    resource_class_kwargs={"schema": ArtistSchema()},
    endpoint="artist"
)
api.add_resource(
    ArtistByNameAPI, 
    "/artists/<name>",
    resource_class_kwargs={"schema": ArtistSchema()},
    endpoint="artist_by_name"
)


#image resources
api.add_resource(
    ArtistImageListAPI,
    "/artists/<int:artist_id>/images",
    resource_class_kwargs={"schema": ImageSchema()},
    endpoint="images"
)

#performance resources
api.add_resource(
    PerformanceListAPI,
    "/performances",
    resource_class_kwargs={"schema": PerformanceSchema()},
    endpoint="performances"
)
api.add_resource(
    PerformanceAPI,
    "/performances/<int:performance_id>",
    resource_class_kwargs={"schema": PerformanceSchema()},
    endpoint="performance"
)
api.add_resource(
    ArtistPerformanceListAPI,
    "/artists/<int:artist_id>/performances",
    resource_class_kwargs={"schema": PerformanceSchema()},
    endpoint="artist_performances"
)


#user resources
api.add_resource(
    UserListAPI,
    "/users",
    resource_class_kwargs={"schema": UserSchema()},
    endpoint="users"
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
    endpoint="venues"
)
api.add_resource(
    VenueAPI,
    "/venues/<int:venue_id>",
    resource_class_kwargs={"schema": VenueSchema()},
    endpoint="venue"
)
api.add_resource(
    VenueByNameAPI,
    "/venues/<name>",
    resource_class_kwargs={"schema": VenueSchema()},
    endpoint="venue_by_name"
)


#Scrapy crawls executed by Celery
api.add_resource(
    CrawlTaskAPI,
    "/crawl",
    endpoint="crawl"
)
api.add_resource(
    CrawlTaskStatusAPI,
    "/crawl_status/<task_id>",
    endpoint="crawl_status"
)
api.add_resource(
    CrawlGroupAPI,
    "/group_crawl",
    endpoint="group_crawl"
)

