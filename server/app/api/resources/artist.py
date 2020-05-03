"""This module contains the artist resource."""


from http import HTTPStatus
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.models import Artist
from app.extensions import db
from app.api.helpers import paginate


class ArtistAPI(Resource):
    """Class to represent a single artist resource."""
    
    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self, artist_id):
        """Return a single artist resource."""
        artist = Artist.query.get(artist_id)
        if artist is None:
            return {"message": "Artist could not be found."}, HTTPStatus.NOT_FOUND
        return self._schema.dump(artist), HTTPStatus.OK

    def put(self, artist_id):
        """Update a single artist resource."""
        json_data = request.get_json()
        try:
            updated_artist = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.messages}, HTTPStatus.BAD_REQUEST
        artist = Artist.query.get(artist_id)
        if artist is None:
            return {"message": "Artist could not be found."}, HTTPStatus.NOT_FOUND
        artist.name = updated_artist.name
        artist.bio = updated_artist.bio
        artist.website = updated_artist.website
        db.session.commit()
        return {}, HTTPStatus.NO_CONTENT

    def delete(self, artist_id):
        """Delete a single artist resource."""
        artist = Artist.query.get(artist_id)
        if artist is None:
            return {"message": "Artist could not be found."}, HTTPStatus.NOT_FOUND
        db.session.delete(artist)
        db.session.commit()
        return {}, HTTPStatus.NO_CONTENT


class ArtistByNameAPI(Resource):
    """Class to represent a single artist resource identified by name."""

    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self, name):
        """Return a single artist resource identified by name."""
        artist = Artist.query.filter_by(name=name).first()
        if artist is None:
            return {"message": "Artist could not be found."}, HTTPStatus.NOT_FOUND
        return self._schema.dump(artist), HTTPStatus.OK


class ArtistListAPI(Resource):
    """Class to represent a collection of artist resources."""
    
    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self):
        """Return all artist resources."""
        query = Artist.query
        return paginate(Artist.__tablename__, query, self._schema), HTTPStatus.OK
        
    def post(self):
        """Create a new artist resource."""
        json_data = request.get_json()
        try:
            new_artist = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.messages}, HTTPStatus.BAD_REQUEST
        existing_artist = Artist.query.filter_by(name=new_artist.name).first()
        if existing_artist is not None:
            return {"message": "Artist already exists."}, HTTPStatus.CONFLICT
        db.session.add(new_artist)
        db.session.commit()
        return self._schema.dump(new_artist), HTTPStatus.CREATED
        
        
