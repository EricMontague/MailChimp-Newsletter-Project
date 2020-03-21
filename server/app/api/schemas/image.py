"""This module contains the image schema."""


from app.extensions import ma
from app.models import Image
from marshmallow import post_load, ValidationError, validate


class ImageSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize Image objects."""

    class Meta:
        model = Image

    id = ma.auto_field(dump_only=True)
    path = ma.auto_field(required=True)
    artist = ma.HyperlinkRelated("artist")

    _links = ma.Hyperlinks({
        "uri": ma.URLFor("image", id="<id>"), "collection": ma.URLFor("image_list")
    })

    @post_load
    def make_object(self, data, **kwargs):
        """Return an image object from the validated data."""
        if data is None:
            raise ValidationError("No data was provided")
        return Image(**data)
