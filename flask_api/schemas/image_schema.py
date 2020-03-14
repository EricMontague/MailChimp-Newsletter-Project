"""This module contains the image schema."""


from ..app import ma
from ..models import Image


class ImageSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize Image objects."""

    class Meta:
        model = Image

    id = ma.auto_field()
    path = ma.auto_field()
    artist = ma.HyperlinkRelated("artists/<int:id>")

    _links = ma.Hyperlink(
        "uri": ma.URLFor("images", id="<int:id>"), "collection": ma.URLFor("images")
    )