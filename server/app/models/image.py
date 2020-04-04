"""This module contains the image model."""


from app.extensions import db


class Image(db.Model):
    """Class to represent an image."""

    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text(), unique=True, index=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)

    def __repr__(self):
        """Return a string representation of the model."""
        return "<Image: %r >" % self.path

