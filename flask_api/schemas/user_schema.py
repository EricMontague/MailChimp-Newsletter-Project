"""This module contains the user schema."""

from ..app import ma
from ..models import User


class UserSchema(ma.SQLAlchemySchema):
    """Class to serialize and deserialize User objects."""

    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.Email()
    password_hash = ma.auto_field()

    _links = ma.Hyperlinks(
        {"uri": ma.URLFor("users", id="<int:id>"), "collection": ma.URLFor("users")}
    )
