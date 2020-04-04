"""This module contains classes to represent image resources."""


from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.models import Image, Artist
from app.extensions import db
from http import HTTPStatus


class ArtistImageListAPI(Resource):
    """Class to represent a collection of image resources
    for an artist.
    """

    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self, artist_id):
        """Return all image resources for a specific artist."""
        artist = Artist.query.get(artist_id)
        if artist is None:
            return {"message": "Artist could not be found."}, HTTPStatus.NOT_FOUND
        images = [artist.image]
        return self._schema.dumps(images, many=True), HTTPStatus.OK

    def put(self, artist_id):
        """Create or replace an image resource for a specific artist."""
        json_data = request.get_json()
        try:
            image = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.messages}, HTTPStatus.BAD_REQUEST
        artist = Artist.query.get(artist_id)
        if artist is None:
            return {"message": "Artist could not be found."}, HTTPStatus.NOT_FOUND
        artist.image = image
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT
