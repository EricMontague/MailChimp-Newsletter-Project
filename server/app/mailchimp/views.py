"""This module contains the endpoints for interacting
with the Mailchimp API.
"""


from flask import Blueprint, jsonify, request
from flask_restful import Api
from flask_jwt_extended import verify_jwt_in_request
from http import HTTPStatus
from app.mailchimp.resources import (
    CampaignReportAPI,
    CampaignListAPI,
    CampaignAPI,
    CampaignActionsAPI,
    CampaignContentAPI,
    SubscriberListsAPI,
    SubscriberListAPI,
    SubscribersAPI,
    SubscriberAPI
)
from app.mailchimp.schemas import CampaignSchema


mailchimp_blueprint = Blueprint("mailchimp", __name__, url_prefix="/api/v1/mailchimp")
api = Api(mailchimp_blueprint)


@mailchimp_blueprint.before_request
def before_request():
    """Before request hook for the api."""
    try:
        verify_jwt_in_request()
    except:
        return jsonify({"message": "Access token is invalid or expired."}), HTTPStatus.UNAUTHORIZED



#Campaign uris
api.add_resource(
    CampaignAPI,
    "/campaigns/<campaign_id>",
    resource_class_kwargs={"schema": CampaignSchema()},
    endpoint="campaign"
)
api.add_resource(
    CampaignListAPI,
    "/campaigns",
    resource_class_kwargs={"schema": CampaignSchema()},
    endpoint="campaigns"
)

#Campaign actions uris
api.add_resource(
    CampaignActionsAPI,
    "/campaigns/<campaign_id>/<action>",
    endpoint="campaign_actions"
)


#Campaign content uris
api.add_resource(
    CampaignContentAPI,
    "/campaigns/<campaign_id>/content",
    endpoint="campaign_content"
)


#Subscriber lists uris
api.add_resource(
    SubscriberListsAPI,
    "/subscriber_lists",
    endpoint="subscriber_lists"
)
api.add_resource(
    SubscriberListAPI,
    "/subscriber_lists/<list_id>",
    endpoint="subscriber_list"
)


#Subscriber uris
api.add_resource(
    SubscribersAPI,
    "/subscriber_lists/<list_id>/subscribers",
    endpoint="subscribers"
)
api.add_resource(
    SubscriberAPI,
    "/subcriber_lists/<list_id>/subscribers/<subscriber_hash>",
    endpoint="subscriber"
)

