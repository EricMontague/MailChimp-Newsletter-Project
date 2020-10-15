"""This module contains the class-based views for creating
and altering subscriber lists using the Mailchimp API.
"""


from flask import request, current_app, url_for
from flask_restful import Resource
from http import HTTPStatus
from mailchimp3.mailchimpclient import MailChimpError



# Note: Mailchimp treats Subscriber lists and subscribers as two separate resources
class SubscriberListsAPI(Resource):
    """Class-based view for creating a new subscriber
    list and getting all subscriber lists from the
    Mailchimp API.
    """

    def get(self):
        """Return all subscriber lists from the Mailchimp API."""
        try:
            subscriber_lists = current_app.mailchimp_client.lists.all()
        except MailChimpError as api_error:
            response = {"errors": {}}
            error_details = api_error.args[0]
            response["errors"]["title"] = error_details["title"]
            response["errors"]["detail"] = error_details["detail"]
            return response, int(error_details["status"])
        for list_ in subscriber_lists:
            list_["_links"] = {
                "uri": url_for("mailchimp.subscriber_list", list_id=list_["id"]),
                "collection": url_for("mailchimp.subscriber_lists")
            }
        return subscriber_lists, HTTPStatus.OK

    def post(self):
        """Create a new subscriber list using the Mailchimp API."""
        json_data = request.get_json()
        try:
            new_subscriber_list = current_app.mailchimp_client.lists.create(data=json_data)
        except MailChimpError as api_error:
            response = {"errors": {}}
            error_details = api_error.args[0]
            response["errors"]["title"] = error_details["title"]
            response["errors"]["detail"] = error_details["detail"]
            return response, int(error_details["status"])
        new_subscriber_list["_links"] = {
            "uri": url_for("mailchimp.subscriber_list", list_id=list_["id"]),
            "collection": url_for("mailchimp.subscriber_lists")
        }
        return new_subscriber_list, HTTPStatus.CREATED


class SubscriberListAPI(Resource):
    """Class-based view for performing CRUD operations on a single
    subscriber list using the Mailchimp API.
    """

    def get(self, list_id):
        """Return a single subscriber list."""
        try:
            subscriber_list = current_app.mailchimp_client.lists.get(list_id=list_id)
        except MailChimpError as api_error:
            response = {"errors": {}}
            error_details = api_error.args[0]
            response["errors"]["title"] = error_details["title"]
            response["errors"]["detail"] = error_details["detail"]
            return response, int(error_details["status"])
        subscriber_list["_links"] = {
            "uri": url_for("mailchimp.subscriber_list", list_id=list_["id"]),
            "collection": url_for("mailchimp.subscriber_lists")
        }
        return subscriber_list, HTTPStatus.OK

    def patch(self, list_id):
        """Update a single attribute of a subscriber list."""
        pass

    def delete(self, list_id):
        """Delete a single subscriber list."""
        pass

