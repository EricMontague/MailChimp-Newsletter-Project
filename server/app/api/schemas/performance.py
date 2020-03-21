"""This module contains the performance schema."""


import datetime as dt
from app.extensions import ma
from app.models import Performance
from marshmallow import post_load, ValidationError, validate, validates_schema


class PerformanceSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize Performance objects."""

    class Meta:
        model = Performance

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(validate=validate.Length(min=1, max=128))
    description = ma.auto_field(validate=validate.Length(min=1))
    url = ma.Url(required=True)
    start_datetime = ma.auto_field(required=True) #iso format by default
    end_datetime = ma.auto_field(required=True) #iso format by default
    artist = ma.HyperlinkRelated("artist")
    venue = ma.HyperlinkRelated("venue")

    _links = ma.Hyperlinks({
        "uri": ma.URLFor("performance", id="<id>"), "collection": ma.URLFor("performance_list")
    })

    @post_load
    def make_object(self, data, **kwargs):
        """Return a performance object from the validated data."""
        if data is None:
            raise ValidationError("No data was provided")
        return Performance(**data)

    @validates_schema
    def validate_datetimes(self, data, **kwargs):
        """Raise a ValidationError if the start_datetime is after
        the end_datetime.
        """
        if data["start_datetime"] > data["end_datetime"]:
            raise ValidationError("'start_datetime' must be after the 'end_datetime'")
    