"""This module contains the artist model."""


from app.extensions import db


class Artist(db.Model):
    """Class to represent an artist."""

    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    bio = db.Column(db.Text(), nullable=True)
    website = db.Column(db.Text(), unique=True, nullable=True)
    performances = db.relationship(
        "Performance", 
        backref="artist", 
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    image = db.relationship(
        "Image", backref="artist", lazy=True, uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self):
        """Return a string representation of the model."""
        return "<Artist: %r>" %(self.name)
        