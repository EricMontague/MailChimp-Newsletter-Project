"""This module contains the class for serializing and deserializing
Campaign models.
"""


from app.extensions import ma
from app.models import Campaign
from marshmallow import post_load, ValidationError, validate


class CampaignSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize campaign objects."""

    class Meta:
        model = Campaign

    mailchimp_id = ma.auto_field(required=True, validate=validate.Length(equal=32))
    sender = ma.HyperlinkRelated("api.user", url_key="user_id")

    _links = ma.Hyperlinks({
        "uri": ma.URLFor("mailchimp.campaign", campaign_id="<mailchimp_id>"),
        "collection": ma.URLFor("mailchimp.campaigns")
    })

    @post_load
    def make_object(self, data, **kwargs):
        """Return a campaign object from the validated data."""
        if data is None:
            raise ValidationError("No data was provided")
        return Campaign(**data)

