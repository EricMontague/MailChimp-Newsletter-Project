"""This module contains helper functions for the api blueprint."""


import os
from flask import current_app
from datetime import datetime


def string_to_date(date_string, format):
    """Given a string date and format, return a 
    corresponding date object.
    """
    try:
        return datetime.strptime(date_string, format).date()
    except ValueError:
        return None


def allowed_file_extension(filename):
    """Return True if the extension of the given file is in the set of
    allowed file extensions.
    """
    if "." not in filename:
        return False
    file_extension = filename.lower().split(".")[-1]
    return file_extension in current_app.config["ALLOWED_EXTENSIONS"]
    

def create_directory(directory):
    """Create the given directory if it doesn't already exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_filepath(filename, version=1):
    """Given a filename and version, return the filepath where
    the file will be stored as a string.
    """
    extensions = current_app.config["ALLOWED_EXTENSIONS"]
    for extension in extensions:
        index = filename.find(extension)
        #creaate new filename in the format of my_old_file_2.jpg
        if index != - 1:
            new_filename = filename[:index - 1] + "_" + str(version) + "." + extension
            break
    filepath = current_app.config["UPLOAD_DIRECTORY"] + "/" + new_filename
    return filepath

