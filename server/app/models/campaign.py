"""This module contains the class to hold data about
Mailchimp campaigns.
"""


from app.extensions import db


class Campaign(db.Model):
    """Class to represent a Mailchimp campaign."""

    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key=True)
    mailchimp_id = db.Column(db.String(32), unique=True, index=True, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __str__(self):
        """Return a string representation of a campaign."""
        return "<Campaign: %s >" % self.mailchimp_id

    