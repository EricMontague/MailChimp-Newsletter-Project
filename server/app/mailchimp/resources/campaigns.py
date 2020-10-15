"""This module contains the class-based views for creating
and altering Mailchimp campaign inforation in the database.
"""


from flask import request
from flask_jwt_extended import current_user
from flask_restful import Resource
from marshmallow import ValidationError
from app.extensions import db
from app.models import Campaign
from http import HTTPStatus
from app.project_helpers import paginate


class CampaignListAPI(Resource):
    """View for retrieving and adding campaigns from the database."""

    def __init__(self, schema):
        self.schema = schema

    def get(self):
        """Return a list of campaigns."""
        query = Campaign.query
        return paginate(Campaign.__tablename__, query, self.schema), HTTPStatus.OK

    def post(self):
        """Create a new campaign model and o the database."""
        json_data = request.get_json()
        json_data["sender_id"] = current_user.id
        try:
            new_campaign = self.schema.load(json_data)
        except ValidationError as err:
            return {"message": err.messages}, HTTPStatus.BAD_REQUEST
        if Campaign.query.filter_by(mailchimp_id=new_campaign.mailchimp_id).first() is not None:
            return {"message": "Campaign already exists."}, HTTPStatus.CONFLICT
        db.session.add(new_campaign)
        db.session.commit()
        return self.schema.dump(new_campaign), HTTPStatus.CREATED
        

class CampaignAPI(Resource):
    """View for updating a single campaign in the database."""

    def __init__(self, schema):
        self.schema = schema
        
    def get(self, campaign_id):
        """Return the campaign with the given id. The id in this case
        is the mailchimp id for the campaign.
        """
        campaign = Campaign.query.filter_by(mailchimp_id=campaign_id).first()
        if campaign is None:
            return {"message": "Campaign could not be found."}, HTTPStatus.NOT_FOUND
        return self.schema.dump(campaign), HTTPStatus.OK

    def delete(self, campaign_id):
        """Delete the given campaign."""
        campaign = Campaign.query.get(campaign_id)
        if campaign is None:
            return {"message": "Campaign could not be found."}, HTTPStatus.NOT_FOUND
        db.session.delete(campaign)
        db.sessioin.commit()
        return {}, HTTPStatus.NO_CONTENT


