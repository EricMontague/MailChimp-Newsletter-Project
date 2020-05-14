"""This module contains the endpoints for interacting
with the Mailchimp API.
"""


from flask import Blueprint, jsonify, request
from flask_restful import Api
from flask_jwt_extended import verify_jwt_in_request
from http import HTTPStatus
from app.mailchimp.resources import CampaignListAPI, CampaignAPI
from app.mailchimp.scheams import CampaignSchema


mailchimp_blueprint = Blueprint("mailchimp", __name__, url_prefix="api/v1/mailchimp")
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
    CampaignListAPI
    "/campaigns",
    resource_class_kwargs={"schema": CampaignSchema()},
    endpoint="campaigns"
)
