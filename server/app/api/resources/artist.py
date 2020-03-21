"""This module contains the artist resource."""


from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.models import Artist
from app.extensions import db
from http import HTTPStatus


class ArtistAPI(Resource):
    """Class to represent a single artist resource."""
    
    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self, artist_id):
        """Return a single artist resource."""
        artist = Artist.query.get(artist_id)
        if artist is None:
            return {"message": "Artist could not be found"}, 
        return self._schema.dump(artist), HTTPStatus.OK

    def put(self, artist_id):
        """Update a single artist resource."""
        json_data = request.get_json()
        try:
            updated_artist = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.message}, HTTPStatus.BAD_REQUEST
        artist = Artist.query.get(artist_id)
        if artist is None:
            return {"message": "Artist could not be found"}, HTTPStatus.NOT_FOUND
        artist.name = updated_artist.name
        artist.bio = updated_artist.bio
        artist.website = updated_artist.website
        db.session.commit()
        return self._schema.dump(artist), HTTPStatus.NO_CONTENT

    def delete(self, artist_id):
        """Delete a single artist resource."""
        artist = Artist.query.get(artist_id)
        if artist is None:
            return {"message": "Artist could not be found"}, HTTPStatus.NOT_FOUND
        db.session.delete(artist)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT


class ArtistListAPI(Resource):
    """Class to represent a collection of artist resources."""
    
    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self):
        """Return all artist resources."""
        artists = Artist.query.all()
        return self._schema.dump(artists, many=True), HTTPStatus.OK

    def post(self):
        """Create a new artist resource."""
        json_data = request.get_json()
        try:
            artist = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.messages}, HTTPStatus.BAD_REQUEST
        db.session.add(artist)
        db.session.commit()
        return self._schema.dump(artist), HTTPStatus.CREATED
        
        
