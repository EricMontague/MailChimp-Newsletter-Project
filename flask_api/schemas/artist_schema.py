"""This module contains the artist schema."""

from ..app import ma
from ..models import Artist
from marshmallow import post_load, ValidationError, validate


class ArtistSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize Artist objects."""

    class Meta:
        model = Artist

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True, validate=validate.Length(min=1, max=64))
    bio = ma.auto_field()
    website = ma.Url()
    performances = ma.List(ma.HyperlinkRelated("performance_list"))
    image = ma.HyperlinkRelated("image")

    _links = ma.Hyperlinks({
        "uri": ma.URLFor("artist", artist_id="<id>"), "collection": ma.URLFor("artist_list")
    })

    @post_load
    def make_object(self, data, **kwargs):
        """Return an artist object from the validated data."""
        if data is None:
            raise ValidationError("No data was provided")
        return Artist(**data)
