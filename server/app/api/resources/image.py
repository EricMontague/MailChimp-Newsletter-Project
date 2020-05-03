"""This module contains classes to represent image resources."""


import os
from flask import request, current_app
from flask_restful import Resource
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from marshmallow import ValidationError
from app.models import Image, Artist
from app.extensions import db
from http import HTTPStatus
from app.api.helpers import allowed_file_extension, create_directory, create_filepath


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
        file = request.files.get("artist_image")
        if file is None:
            return (
                {"message": "Could not find an image file in the request."},
                HTTPStatus.BAD_REQUEST,
            )
        if file.filename == "":
            return {"message": "No selected file."}, HTTPStatus.BAD_REQUEST
        if not allowed_file_extension(file.filename):
            return (
                {
                    "message": f"File extension not allowed. Valid extensions include: {list(current_app.config['ALLOWED_FILE_EXTENSIONS'])}"
                },
                HTTPStatus.BAD_REQUEST,
            )
        filename = secure_filename(file.filename)
        create_directory(current_app.config["UPLOAD_DIRECTORY"])
        artist_image = artist.image
        # creating new image for artist
        if artist_image is None:
            existing_image = Image.query.filter_by(original_filename=filename).first()
            if existing_image is None:
                version = 1
            # another artist already has this image
            # need to increment the version number when saving the image
            else:
                version = existing_image.version + 1
        # replacing existing image
        else:
            version = 1
            # duplicate image, no action is needed
            if artist_image.original_filename == filename:
                return "", HTTPStatus.NO_CONTENT
            else: #not a duplicate, need to delete the current image from filesystem to make room
                if os.path.exists(artist.image.path):
                    os.remove(artist.image.path)
        destination = create_filepath(filename, version=version)
        file.save(destination)
        image = Image(original_filename=filename, path=destination, version=version)
        artist.image = image
        db.session.commit()
        return {}, HTTPStatus.NO_CONTENT

