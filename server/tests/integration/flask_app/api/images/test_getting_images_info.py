"""This module contains tests for sending GET requests to the image endpoints."""


from pytest import mark
from flask_app.utils import get_headers

def test_getting_list_of_images_by_authorized_user(flask_test_client, json, auth, user, artist, image):
    """Test to ensure that a list of image resources can be
    successfully retrieved.
    """
    artist.image = image
    expected_fields = {
        "path", "artist"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/artists/{artist.id}/images",
        headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert isinstance(json.loads(response.json), list)
    assert json.loads(response.json)[0].keys() == expected_fields
    assert json.loads(response.json)[0]["path"] == artist.image.path
    assert json.loads(response.json)[0]["artist"] == f"/api/v1/artists/{artist.id}"


def test_getting_list_of_images_without_token_must_fail(flask_test_client, artist):
    """Test to ensure that an unauthorized user (no token) cannot get
    image resources
    """
    response = flask_test_client.get(
        f"/api/v1/artists/{artist.id}/images",
        headers=get_headers() #no token
    )
    assert response.status == "401 UNAUTHORIZED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Access token is invalid or expired."


#You shouldn't be able to request an image for an artist that doesn't exist
def test_artist_not_found(flask_test_client, auth, user):
    """Test to ensure that a 404 response is returned
    if an artist resource doesn't exist resource does not exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        "/api/v1/artists/100/images",
        headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Artist could not be found."
