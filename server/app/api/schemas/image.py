"""This module contains the image schema."""


from app.extensions import ma
from app.models import Image
from marshmallow import post_load, ValidationError, validate


class ImageSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize Image objects."""

    class Meta:
        model = Image

    path = ma.auto_field(required=True, validate=validate.Length(min=1, max=256))
    artist = ma.HyperlinkRelated("api.artist", url_key="artist_id")

    @post_load
    def make_object(self, data, **kwargs):
        """Return an image object from the validated data."""
        if data is None:
            raise ValidationError("No data was provided")
        return Image(**data)

