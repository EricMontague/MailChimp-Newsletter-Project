"""This module contains the venue schema."""


from ..app import ma
from ..models import Venue


class VenueSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize Venue objects."""

    class Meta:
        model = Venue
    
    id = ma.auto_field()
    name = ma.auto_field()
    street_address = ma.auto_field()
    city = ma.auto_field()
    state = ma.auto_field()
    zip_code = ma.auto_field()
    performances = ma.List(ma.HyperlinkRelated("performances"))

    _links = ma.Hyperlink(
        "uri": ma.URLFor("venues", id="<int:id>"), "collection": ma.URLFor("venues")
    )