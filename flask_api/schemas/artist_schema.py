"""This module contains the artist schema."""

from ..app import ma
from ..models import Artist


class ArtistSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize Artist objects."""

    class Meta:
        model = Artist

    id = ma.auto_field()
    name = ma.auto_field()
    bio = ma.auto_field()
    website = ma.Url()
    performances = ma.List(ma.HyperlinkRelated("performances"))
    image = ma.HyperlinkRelated("images/<int:id>")

    _links = ma.Hyperlinks(
        "uri": ma.URLFor("artists", id="<int:id>"), "collection": ma.URLFor("artists")
    )
