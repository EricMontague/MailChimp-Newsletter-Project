"""This module contains the artist schema."""


from flask import request
from app.extensions import ma
from app.models import Artist
from marshmallow import post_load, ValidationError, validate, validates_schema


class ArtistSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize Artist objects."""

    class Meta:
        model = Artist

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True, validate=validate.Length(min=1, max=64))
    bio = ma.auto_field()
    website = ma.Url()
    performances = ma.List(ma.HyperlinkRelated("api.performance", url_key="performance_id"))
    image = ma.HyperlinkRelated("api.image_list", url_key="artist_id")

    _links = ma.Hyperlinks({
        "uri": ma.URLFor("api.artist", artist_id="<id>"), "collection": ma.URLFor("api.artist_list")
    })

    @validates_schema
    def validate_on_put_request(self, data, **kwargs):
        """Raise a ValidationError if certain fields are not sent
        during a PUT request.
        """
        if request.method == "PUT":
            if "bio" not in data or "website" not in data:
                raise ValidationError("Missing one or more fields.")

    @post_load
    def make_object(self, data, **kwargs):
        """Return an artist object from the validated data."""
        if data is None:
            raise ValidationError("No data was provided")
        return Artist(**data)
