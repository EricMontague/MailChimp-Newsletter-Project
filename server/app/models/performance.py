"""This module contains the performance model."""


from app.extensions import db


class Performance(db.Model):
    """Class to represent a performance."""

    __tablename__ = "performances"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    url = db.Column(db.Text(), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)

    def __repr__(self):
        """Return a string representation of the model."""
        return "<Performance: %r>" % self.title
        