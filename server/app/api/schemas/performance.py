"""This module contains the performance schema."""


from datetime import date
from app.extensions import ma
from app.models import Performance
from marshmallow import post_load, ValidationError, validate, validates_schema, validates


class PerformanceSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize Performance objects."""

    class Meta:
        model = Performance

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True, validate=validate.Length(min=1, max=128))
    description = ma.auto_field(validate=validate.Length(min=1))
    url = ma.Url(required=True)
    start_datetime = ma.auto_field(required=True, format="%m/%d/%Y %H:%M")
    end_datetime = ma.auto_field(required=True, format="%m/%d/%Y %H:%M")
    artist_id = ma.auto_field(required=True, load_only=True)
    venue_id = ma.auto_field(required=True, load_only=True)
    artist = ma.HyperlinkRelated("api.artist", url_key="artist_id")
    venue = ma.HyperlinkRelated("api.venue", url_key="venue_id")

    _links = ma.Hyperlinks(
        {
            "uri": ma.URLFor("api.performance", performance_id="<id>"),
            "collection": ma.URLFor("api.performance_list"),
        }
    )

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
        #start date is after end date
        if data["start_datetime"].date() > data["end_datetime"].date():
            raise ValidationError("Start date must be before end date.")
        #start date and end date are the same day, but start time is after end time
        elif data["start_datetime"].date() == data["end_datetime"].date() \
                and data["start_datetime"].time() > data["end_datetime"].time():
                raise ValidationError("Start time must be before end time.")
