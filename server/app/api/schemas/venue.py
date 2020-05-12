"""This module contains the venue schema."""


from app.extensions import ma
from app.models import Venue
from marshmallow import post_load, ValidationError, validate


STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


class VenueSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize Venue objects."""

    class Meta:
        model = Venue
    
    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True, validate=validate.Length(min=1, max=64))
    street_address = ma.auto_field(required=True, validate=validate.Length(min=1, max=64))
    city = ma.auto_field(required=True, validate=validate.Length(min=1, max=64))
    state = ma.auto_field(required=True, validate=[validate.Length(equal=2), validate.OneOf(STATES)])
    zip_code = ma.auto_field(required=True, validate=validate.Length(min=5, max=10))
    performances = ma.List(ma.HyperlinkRelated("api.performance", url_key="performance_id"))

    _links = ma.Hyperlinks({
        "uri": ma.URLFor("api.venue", venue_id="<id>"), "collection": ma.URLFor("api.venues")
    })

    @post_load
    def make_object(self, data, **kwargs):
        """Return a venue object from the validated data."""
        if data is None:
            raise ValidationError("No data was provided")
        return Venue(**data)

    