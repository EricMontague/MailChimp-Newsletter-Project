"""This module contains tests for sending GET requests to the image endpoints."""


from pytest import mark
from flask_app.utils import get_headers


def test_getting_single_image_by_authorized_user(flask_test_client, auth, json, user, image, artist):
    """Test to ensure that a single image resource can be
    successfully retrieved.
    """
    expected_fields = {
        "id", "path", "artist", "_links"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/images/{image.id}",
        headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == expected_fields
    assert response.json["id"] == image.id
    assert response.json["path"] == image.path
    assert response.json["artist"] == f"/api/v1/artists/{artist.id}"
    assert response.json["_links"]["uri"] == f"/api/v1/images/{image.id}"
    assert response.json["_links"]["collection"] == f"/api/v1/images"
    

def test_getting_single_image_without_token_must_fail(flask_test_client, image):
    """Test to ensure that an unauthorized  user (no token) cannot get
    an image resource.
    """
    response = flask_test_client.get(
        f"/api/v1/images/{image.id}",
        headers=get_headers() #no token sent
    )
    assert response.status == "401 UNAUTHORIZED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Access token is invalid or expired."


def test_getting_list_of_images_by_authorized_user(flask_test_client, json, auth, user, image, artist):
    """Test to ensure that a list of image resources can be
    successfully retrieved.
    """
    expected_fields = {
        "id", "path", "artist", "_links"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/images",
        headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == {"images", "prev", "next", "total"}
    assert isinstance(json.loads(response.json["images"]), list)
    assert set(json.loads(response.json["images"])[0].keys()) == expected_fields
    assert response.json["total"] == 1
    assert response.json["prev"] is None
    assert response.json["next"] is None
    assert json.loads(response.json["images"])[0]["id"] == image.id
    assert json.loads(response.json["images"])[0]["path"] == image.path
    assert json.loads(response.json["images"])[0]["artist"] == f"/api/v1/artists/{artist.id}"
    assert json.loads(response.json["images"])[0]["_links"]["uri"] == f"/api/v1/images/{image.id}"    
    assert json.loads(response.json["images"])[0]["_links"]["collection"] == "/api/v1/images"


def test_getting_list_of_images_without_token_must_fail(flask_test_client):
    """Test to ensure that an unauthorized user (no token) cannot get
    image resources
    """
    response = flask_test_client.get(
        f"/api/v1/images",
        headers=get_headers() #no token
    )
    assert response.status == "401 UNAUTHORIZED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Access token is invalid or expired."


def test_image_not_found(flask_test_client, auth, user):
    """Test to ensure that a 404 response is returned
    if an image resource does not exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/images/100",
        headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Image could not be found."
