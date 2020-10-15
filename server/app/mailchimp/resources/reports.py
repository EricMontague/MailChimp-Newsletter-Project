"""This module contains the class-based views for retrieving
data about campaigns from the Mailchimp API.
"""


from flask import request, current_app, url_for
from flask_restful import Resource
from http import HTTPStatus
from mailchimp3.mailchimpclient import MailChimpError


class CampaignReportAPI(Resource):
    """Class-based view for retrieving data
    on a specific campaign.
    """

    def __init__(self, fields):
        self.fields = fields # fields to request from the api
    
    def get(self, campaign_id):
        """Return stats about the campaign associated with 
        the given id.
        """
        try:
            report = current_app.mailchimp_client.reports.get(
                campaign_id=campaign_id,
                fields=self.fields
            )
        except MailChimpError as api_error:
            response = {"errors": {}}
            error_details = api_error.args[0]
            response["errors"]["title"] = error_details["title"]
            response["errors"]["detail"] = error_details["detail"]
            return response, int(error_details["status"])
        report["_links"] = {
            "uri": url_for("mailchimp.reports", campaign_id=campaign_id)
        }
        return report, HTTPStatus.OK


