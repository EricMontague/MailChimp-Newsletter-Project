"""This module contains the performance schema."""


from ..app import ma
from ..models import Performance


class PerformanceSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize Performance objects."""

    class Meta:
        model = Performance
    
    id = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    url = ma.Url()
    start_datetime = ma.auto_field()
    end_datetime = ma.auto_field()
    artist = ma.HyperlinkRelated("artists/<int:id>")
    venue = ma.HyperlinkRelated("venues/<int:id>")

    _links = ma.Hyperlink(
        "uri": ma.URLFor("performances", id="<int:id>"), "collection": ma.URLFor("performances")
    )
    