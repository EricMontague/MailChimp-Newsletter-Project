"""This package contains the class-based views for interacting
with the Mailchimp API.
"""

from app.mailchimp.resources.reports import CampaignReportAPI
from app.mailchimp.resources.campaigns import (
    CampaignListAPI,
    CampaignAPI,
    CampaignActionsAPI,
    CampaignContentAPI
)
from app.mailchimp.resources.subscriber_lists import (
    SubscriberListsAPI,
    SubscriberListAPI
)
from app.mailchimp.resources.subscribers import (
    SubscribersAPI,
    SubscriberAPI
)

