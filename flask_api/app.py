"""This module contains the application instance as well as all flask extensions
and other dependencies.
"""


import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .config import config
from flask_migrate import Migrate


app = Flask(__name__.split('.')[0])
app.config.from_object(config[os.environ.get("APP_CONFIG", "default")])
api = Api(app, prefix="/api/v1")
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


from .models import User, Artist, Performance, Venue, Image


from .schemas.artist_schema import ArtistSchema
from .schemas.image_schema import ImageSchema
from .schemas.performance_schema import PerformanceSchema
from .schemas.user_schema import UserSchema
from .schemas.venue_schema import VenueSchema


from .resources.artist_resource import ArtistResource, ArtistListResource
from .resources.image_resource import ImageResource, ImageListResource
from .resources.performance_resource import PerformanceResource, PerformanceListResource
from .resources.user_resource import UserResource, UserListResource
from .resources.venue_resource import VenueResource, VenueListResource


#artist resources
api.add_resource(
    ArtistListResource, 
    "/artists", 
    resource_class_kwargs={"schema": ArtistSchema()},
    endpoint="artist_list"
)
api.add_resource(
    ArtistResource, 
    "/artists/<int:artist_id>",
    resource_class_kwargs={"schema": ArtistSchema()},
    endpoint="artist"
)


#image resources
api.add_resource(
    ImageListResource,
    "images",
    resource_class_kwargs={"schema": ImageSchema()},
    endpoint="image_list"
)
api.add_resource(
    ImageResource,
    "images/<int:image_id>",
    resource_class_kwargs={"schema": ImageSchema()},
    endpoint="image"
)


#performance resources
api.add_resource(
    PerformanceListResource,
    "performances",
    resource_class_kwargs={"schema": PerformanceSchema()},
    endpoint="performance_list"
)
api.add_resource(
    PerformanceResource,
    "performances/<int:performance_id>",
    resource_class_kwargs={"schema": PerformanceSchema()},
    endpoint="performance"
)


#user resources
api.add_resource(
    UserListResource,
    "users",
    resource_class_kwargs={"schema": UserSchema()},
    endpoint="user_list"
)
api.add_resource(
    UserResource,
    "users/<int:user_id>",
    resource_class_kwargs={"schema": UserSchema()},
    endpoint="user"
)


#venue resources
api.add_resource(
    VenueListResource,
    "venues",
    resource_class_kwargs={"schema": VenueSchema()},
    endpoint="venue_list"
)
api.add_resource(
    VenueResource,
    "venues/<int:venue_id>",
    resource_class_kwargs={"schema": VenueSchema()},
    endpoint="venue"
)



@app.shell_context_processor
def make_shell_context():
    """Allow the models and database instance to be automatically imported
    when a flask shell session is started
    """
    return dict(
        db=db,
        User=User,
        Artist=Artist,
        Performance=Performance,
        Venue=Venue,
        Image=Image
    )


if __name__ == "__main__":
    app.run(debug=True)
