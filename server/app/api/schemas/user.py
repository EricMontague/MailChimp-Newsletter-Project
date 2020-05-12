"""This module contains the user schema."""


from flask import request
from app.extensions import ma
from app.models import User
from marshmallow import post_load, ValidationError, validate


class UserSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize User objects."""

    class Meta:
        model = User

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(required=True, validate=validate.Length(min=1, max=64))
    email = ma.Email(required=True, validate=validate.Length(min=1, max=64))
    password = ma.Str(required=True, validate=validate.Length(8, 30), load_only=True)

    _links = ma.Hyperlinks({
        "uri": ma.URLFor("api.user", user_id="<id>"), "collection": ma.URLFor("api.users")
    })
       
    @post_load
    def make_object(self, data, **kwargs):
        """Return a user object from the validated data."""
        if data is None:
            raise ValidationError("No data was provided")
        return User(**data)

