"""This module contains the performance resources."""

from flask import request
from flask_restful import Resource
from sqlalchemy import func
from marshmallow import ValidationError
from app.models import Performance, Artist
from app.extensions import db
from http import HTTPStatus
from app.api.helpers import paginate, string_to_date


class PerformanceAPI(Resource):
    """Class to represent a single performance resource."""

    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self, performance_id):
        """Return a single performance resource."""
        performance = Performance.query.get(performance_id)
        if performance is None:
            return {"message": "Performance could not be found."}, HTTPStatus.NOT_FOUND
        return self._schema.dump(performance), HTTPStatus.OK

    def put(self, performance_id):
        """Update a single performance resource."""
        json_data = request.get_json()
        try:
            updated_performance = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.messages}, HTTPStatus.BAD_REQUEST
        performance = Performance.query.get(performance_id)
        if performance is None:
            return {"message": "Performance not found."}, HTTPStatus.NOT_FOUND
        performance.title = updated_performance.title
        performance.description = updated_performance.description
        performance.url = updated_performance.url
        performance.start_datetime = updated_performance.start_datetime
        performance.end_datetime = updated_performance.end_datetime
        performance.artist_id = updated_performance.artist_id
        performance.venue_ud = updated_performance.venue_id
        db.session.commit()
        return self._schema.dump(performance), HTTPStatus.NO_CONTENT

    def delete(self, performance_id):
        """Delete a single performance resource."""
        performance = Performance.query.get(performance_id)
        if performance is None:
            return {"message": "Performance could not be found."}, HTTPStatus.NOT_FOUND
        db.session.delete(performance)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT


class PerformanceListAPI(Resource):
    """Class to represent the collection of performance resources."""

    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self):
        """Return the collection of performance resources."""
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        # only provided with either start date or end date
        if (
            start_date is not None
            and end_date is None
            or start_date is None
            and end_date is not None
        ):
            return (
                {"message": "Please provide both a start and an end date."},
                HTTPStatus.BAD_REQUEST,
            )
        # Both start and end dates provided
        if start_date is not None and end_date is not None:
            start_date = string_to_date(start_date, "%m/%d/%Y")
            end_date = string_to_date(end_date, "%m/%d/%Y")
            if start_date is None:
                return {
                    "message": {"start_date": "Incorrectly formatted date."}
                }, HTTPStatus.BAD_REQUEST
            elif end_date is None:
                return {
                    "message": {"end_date": "Incorrectly formatted date."}
                }, HTTPStatus.BAD_REQUEST
            # filter query by start and end date
            query = Performance.query.filter(
                func.Date(Performance.start_datetime) >= start_date,
                func.Date(Performance.start_datetime) <= end_date
            )
        else:  # no query string parameters
            query = Performance.query
        return paginate(Performance.__tablename__, query, self._schema), HTTPStatus.OK
        

    def post(self):
        """Create a new performance resource."""
        json_data = request.get_json()
        try:
            performance = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.messages}, HTTPStatus.BAD_REQUEST
        db.session.add(performance)
        db.session.commit()
        return self._schema.dump(performance), HTTPStatus.CREATED


# Todo: Figure out how to refactor this because this is essentially duplicate code
class ArtistPerformanceListAPI(Resource):
    """Class to represent the collection of performance resources by 
    a specific artist.
    """

    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self, artist_id):
        """Return the collection of performance resources
        for a specific artist.
        """
        artist = Artist.query.get(artist_id)
        if artist is None:
            return {"message": "Artist could not be found."}, HTTPStatus.NOT_FOUND
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        # only provided with either start date or end date
        if (
            start_date is not None
            and end_date is None
            or start_date is None
            and end_date is not None
        ):
            return (
                {"message": "Please provide both a start and an end date."},
                HTTPStatus.BAD_REQUEST,
            )
        # Both start and end dates provided
        if start_date is not None and end_date is not None:
            start_date = string_to_date(start_date, "%m/%d/%Y")
            end_date = string_to_date(end_date, "%m/%d/%Y")
            if start_date is None:
                return {
                    "message": {"start_date": "Incorrectly formatted date."}
                }, HTTPStatus.BAD_REQUEST
            elif end_date is None:
                return {
                    "message": {"end_date": "Incorrectly formatted date."}
                }, HTTPStatus.BAD_REQUEST
            # filter query by start and end date
            query = Performance.query.filter(
                func.Date(Performance.start_datetime) >= start_date,
                func.Date(Performance.start_datetime) <= end_date
            )
        else:  # no query string parameters
            query = Performance.query
        return paginate(Performance.__tablename__, query, self._schema), HTTPStatus.OK

