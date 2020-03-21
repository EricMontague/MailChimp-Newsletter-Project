"""This module contains the venue resource."""


from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.models import Venue
from app.extensions import db
from http import HTTPStatus


class VenueAPI(Resource):
    """Class to represent a single venue resource."""
    
    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self, venue_id):
        """Return a single venue resource."""
        venue = Venue.query.get(venue_id)
        if venue is None:
            return {"message": "Venue could not be found"}, HTTPStatus.NOT_FOUND
        return self._schema.dump(venue), HTTPStatus.OK

    def put(self, venue_id):
        """Update a single venue resource."""
        json_data = request.get_json()
        try:
            updated_venue = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.message}, HTTPStatus.BAD_REQUEST
        venue = Venue.query.get(venue_id)
        if venue is None:
            return {"message": "Venue could not be found"}, HTTPStatus.NOT_FOUND
        venue.name = updated_venue.name
        venue.street_address = updated_venue.street_address
        venue.city = updated_venue.city
        venue.state = updated_venue.state
        venue.zip_code = updated_venue.zip_code
        db.session.commit()
        return self._schema.dump(venue), HTTPStatus.NO_CONTENT

    def delete(self, venue_id):
        """Delete a single venue resource."""
        venue = Venue.query.get(venue_id)
        if venue is None:
            return {"message": "Venue could not be found"}, HTTPStatus.NOT_FOUND
        db.session.delete(venue)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT


class VenueListAPI(Resource):
    """Class to represent a collection of venue resources."""
    
    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self):
        """Return all venue resources."""
        venues = Venue.query.all()
        return self._schema.dump(venues, many=True), HTTPStatus.OK

    def post(self):
        """Create a new venue resource."""
        json_data = request.get_json()
        try:
            venue = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.messages}, HTTPStatus.BAD_REQUEST
        db.session.add(venue)
        db.session.commit()
        return self._schema.dump(venue), HTTPStatus.CREATED
        
        
