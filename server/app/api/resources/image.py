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
from app.api.helpers import allowed_file_extension, create_directory


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
        create_directory(current_app.config["UPLOAD_DIRECTORY"])
        #delete the artist's current image from the directory if one exists
        if artist.image is not None:
            try:
                os.remove(artist.image.path)
            except FileNotFoundError:
                pass
        filename = secure_filename(file.filename)
        destination = current_app.config["UPLOAD_DIRECTORY"] + "/" + filename
        file.save(destination)
        #the below block isn't in the above if statement because I want to separate out the
        #file system operations from the database operations
        if artist.image is None:
            image = Image(path=destination)
            artist.image = image
        else:
            artist.image.path = destination 
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT
