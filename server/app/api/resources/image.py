"""This module contains classes to represent image resources."""


import os
from flask import request, current_app
from flask_restful import Resource
from werkzeug.utils import secure_filename
from marshmallow import ValidationError
from app.models import Image, Artist
from app.extensions import db
from http import HTTPStatus
from app.api.helpers import allowed_file_extension


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
        artist = Artist.query.get(artist_id)
        if artist is None:
            return {"message": "Artist could not be found."}, HTTPStatus.NOT_FOUND
        file = request.files.get("files")
        if file is None:
            return (
                {"message": "Could not find an image file in the request."},
                HTTPStatus.BAD_REQUEST,
            )
        if not allowed_file_extension(file.filename):
            return (
                {
                    "message": f"File extension not allowed. Valid extensions include: {list(current_app.config['ALLOWED_FILE_EXTENSIONS'])}"
                },
                HTTPStatus.BAD_REQUEST,
            )
        #delete the artist's current image from the directory if one exists
        if artist.image is not None:
            try:
                os.remove(artist.image.path)
            except FileNotFoundError:
                pass
        filename = secure_filename(file.filename)
        file.save(current_app.config["UPLOAD_FOLDER"], filename)
        image = Image(
            path=current_app.config["UPLOAD_FOLDER"] + "/" + filename
        )
        artist.image = image
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT
