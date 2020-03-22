"""This module contains the performance resources."""

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.models import Performance
from app.extensions import db
from http import HTTPStatus
from app.api.helpers import paginate


class PerformanceAPI(Resource):
    """Class to represent a single performance resource."""

    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self, performance_id):
        """Return a single performance resource."""
        performance = Performance.query.get(performance_id)
        if performance is None:
            return {"message": "Performance not found"}, HTTPStatus.NOT_FOUND
        return self._schema.dump(performance), HTTPStatus.OK

    def put(self, performance_id):
        """Update a single performance resource."""
        json_data = request.get_json()
        try:
            updated_performance = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.message}, HTTPStatus.BAD_REQUEST
        performance = Performance.query.get(performance_id)
        if performance is None:
            return {"message": "Performance not found"}, HTTPStatus.NOT_FOUND
        performance.title = updated_performance.title
        performance.description = updated_performance.description
        performance.url = updated_performance.url
        performance.start_datetime = updated_performance.start_datetime
        performance.end_datetime = updated_performance.end_datetime
        db.session.commit()
        return self._schema.dump(performance), HTTPStatus.NO_CONTENT

    def delete(self, performance_id):
        """Delete a single performance resource."""
        performance = Performance.query.get(performance_id)
        if performance is None:
            return {"message": "Performance not found"}, HTTPStatus.NOT_FOUND
        db.session.delete(performance)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT


class PerformanceListAPI(Resource):
    """Class to represent the collection of performance resources."""

    def __init__(self, **kwargs):
        self._schema = kwargs["schema"]

    def get(self):
        """Return the collection of performance resources."""
        return paginate(Performance, self._schema), HTTPStatus.OK

    def post(self):
        """Create a new performance resource."""
        json_data = request.get_json()
        try:
            performance = self._schema.load(json_data)
        except ValidationError as err:
            return {"message": err.message}, HTTPStatus.BAD_REQUEST
        db.session.add(performance)
        db.session.commit()
        return self._schema.dump(performance), HTTPStatus.CREATED

