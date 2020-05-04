"""This module contains the final application instance after it has been created
and configured.
"""


import os
import click
from app import create_app
from app.models import User, Artist, Performance, Venue, Image
from app.extensions import db


app = create_app(os.environ.get("FLASK_CONFIG") or "default")


@app.cli.command()
def create_tables():
    """Create all database tables."""
    db.create_all()


@app.cli.command()
def drop_tables():
    """Drop all database tables."""
    db.drop_all()


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


