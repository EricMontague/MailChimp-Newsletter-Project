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
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


from .models import User, Artist, Performance, Venue, Image


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
