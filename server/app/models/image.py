"""This module contains the image model."""


from app.extensions import db


class Image(db.Model):
    """Class to represent an image."""

    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text(), unique=True, index=True, nullable=False)
    original_filename = db.Column(db.Text(), index=True, nullable=False)
    version = db.Column(db.Integer, default=1, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)

    def __str__(self):
        """Return a string representation of the model."""
        return "<Image: %s >" % self.path

