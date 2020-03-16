"""This module contains classes to represent image resources."""


from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from ..models import Image
from ..app import db
from ..http_status_codes import HTTPStatusCode


class ImageResource(Resource):
    """Class to represent a single image resource."""
    
    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self, image_id):
        """Return a single image resource."""
        image = Image.query.get(image_id)
        if image is None:
            return {"message": "Image not found"}, HTTPStatusCode.NOT_FOUND
        return self._schema.dump(image), HTTPStatusCode.OK

    def put(self, image_id):
        """Update a single image resource."""
        json_data = request.get_json()
        try:
            updated_image = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.message}, HTTPStatusCode.BAD_REQUEST
        image = Image.query.get(image_id)
        if image is None:
            return {"message": "Image not found"}, HTTPStatusCode.NOT_FOUND
        image.path = updated_image.path
        db.session.commit()
        return self._schema.dump(image), HTTPStatusCode.NO_CONTENT

    def delete(self, image_id):
        """Delete a single image resource."""
        image = Image.query.get(image_id)
        if image is None:
            return {"message": "Image not found"}, HTTPStatusCode.NOT_FOUND
        db.session.delete(image)
        db.session.commit()
        return "", HTTPStatusCode.NO_CONTENT
        

class ImageListResource(Resource):
    """Class to represent a collection of image resources."""

    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self):
        """Return all image resources."""
        images = Image.query.all()
        return self._schema.dump(images, many=True), HTTPStatusCode.OK

    def post(self):
        """Create a new image resource."""
        json_data = request.get_json()
        try:
            image = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.message}, HTTPStatusCode.BAD_REQUEST
        db.session.add(image)
        db.session.commit()
        return self._schema.dump(image), HTTPStatusCode.CREATED

    