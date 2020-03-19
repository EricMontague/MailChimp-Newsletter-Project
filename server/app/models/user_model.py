"""This module contains the user model."""


from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """Class to represent a user."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=True, nullable=False)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Set the password hash attribute."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Return True if the correct password is provided by the user."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """Return a string representation of the model."""
        return "<User: %r>" % self.username
        