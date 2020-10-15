"""This module contains the class-based views for adding and
removing subscribers from subscriber lists using the Mailchimp API.
"""


from flask import request, current_app, url_for
from flask_restful import Resource
from http import HTTPStatus
from mailchimp3.mailchimpclient import MailChimpError


# Note: Mailchimp treats Subscriber lists and subscribers as two separate resources
class SubscribersAPI(Resource):
    """View to retrieve all of the subscribers in a list
    and add a subscriber to a list.
    """

    def get(self, list_id):
        """Return all subscribers that are in the given list."""
        try:
            subscribers = current_app.mailchimp_client.lists.members.all(list_id=list_id)
        except MailChimpError as api_error:
            response = {"errors": {}}
            error_details = api_error.args[0]
            response["errors"]["title"] = error_details["title"]
            response["errors"]["detail"] = error_details["detail"]
            return response, int(error_details["status"])
        for subscriber in subscribers:
            subscriber["_links"] = {
                "uri": url_for("mailchimp.subscriber", list_id=list_id, subscriber_hash=subscriber["subscriber_hash"]),
                "collection": url_for("mailchimp.subscribers", list_id=list_id)
            }
        return subscribers, HTTPStatus.OK

    def post(self, list_id):
        """Add a new subscriber to the given list."""
        json_data = request.get_json()
        try:
            subscriber = current_app.mailchimp_client.lists.members.create(lists_id=list_id, data=json_data)
        except MailChimpError as api_error:
            response = {"errors": {}}
            error_details = api_error.args[0]
            response["errors"]["title"] = error_details["title"]
            response["errors"]["detail"] = error_details["detail"]
            return response, int(error_details["status"])
        subscriber["_links"] = {
            "uri": url_for("mailchimp.subscriber", list_id=list_id, subscriber_hash=subscriber["subscriber_hash"]),
            "collection": url_for("mailchimp.subscribers", list_id=list_id)
        }
        return subscriber, HTTPStatus.CREATED


class SubscriberAPI(Resource):
    """View to performa CRUD operations on a single
    subscriber through the Mailchimp API.
    """

    def get(self, list_id, subscriber_hash):
        """Return a single subscriber from the given list."""
        try:
            subscriber = current_app.mailchimp_client.lists.members.get(list_id=list_id, subscriber_hash=subscriber_hash)
        except MailChimpError as api_error:
            response = {"errors": {}}
            error_details = api_error.args[0]
            response["errors"]["title"] = error_details["title"]
            response["errors"]["detail"] = error_details["detail"]
            return response, int(error_details["status"])
        subscriber["_links"] = {
            "uri": url_for("mailchimp.subscriber", list_id=list_id, subscriber_hash=subscriber["subscriber_hash"]),
            "collection": url_for("mailchimp.subscribers", list_id=list_id)
        }
        return subscriber, HTTPStatus.OK

    def post(self, list_id, subscriber_hash):
        """Permanently delete a subscriber from a list."""
        pass

    def put(self, list_id, subscriber_hash):
        """Update a single subscriber in the given list."""
        pass

    def delete(self, list_id, subscriber_hash):
        """Archive the given list member in the given list.
        This will not actually delete a subscriber, but instead
        will remove them from the mailing list.
        """
        pass

