"""This module contains the SQLAlchemy model for a venue."""


from app.extensions import db


class Venue(db.Model):
    """Class to represent a venue or location of a performance."""

    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    street_address = db.Column(db.String(64), unique=True, index=True, nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    performances = db.relationship(
        "Performance", 
        backref="venue", 
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        """Return a string representation of the model."""
        return "<Venue: %r>" % self.name
        