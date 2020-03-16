"""This module contains all of the SQLAlchemy models for the application."""


from .app import db
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


class Image(db.Model):
    """Class to represent an image."""

    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text(), unique=True, index=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)

    def __repr__(self):
        """Return a string representation of the model."""
        return "<Image: %r >" % self.path
