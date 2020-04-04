"""This module contains tests for modifying image resources."""


from pytest import mark
from flask_app.utils import get_headers
from app.models import Image


def test_create_new_artist_image_with_valid_data(flask_test_client, auth, user, json, db, artist):
    """Test that a new artist image resource can be succesfully created
    when valid data is sent to the api.
    """
    image_object = {
        "path": "/Users/fakeuser2/test_project/app/static"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/artists/{artist.id}/images",
        headers=get_headers(token),
        data=json.dumps(image_object)  
    )
    assert response.status == "204 NO CONTENT"
    assert response.content_type == "application/json"
    assert response.get_data(as_text=True) == ""
   
    
    #Cleanup
    new_image = Image.query.filter_by(path=image_object["path"]).first()
    assert new_image is not None
    assert new_image.artist_id == artist.id
    db.session.delete(new_image)


@mark.parametrize(
    "test_input, expected",
    [
        (
            {"path": None},
            {"incorrect_field": "path", "message": ["Field may not be null."]}
        ),
        (
            {"path": "/Users/testuser/project" * 20},
            {"incorrect_field": "path", "message": ["Length must be between 1 and 256."]}
        ),
        (
            {"path": ""},
            {"incorrect_field": "path", "message": ["Length must be between 1 and 256."]}
        ),
        (
            {},
            {"incorrect_field": "path", "message": ["Missing data for required field."]}
        )
    ]
)
def test_create_new_image_with_invalid_data_must_fail(flask_test_client, auth, user, artist, json, test_input, expected):
    """Test that a new image resource cannot be created
    if invalid data is passed to the api.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/artists/{artist.id}/images",
        headers=get_headers(token),
        data=json.dumps(test_input)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"][expected["incorrect_field"]] == expected["message"]

    if test_input.get("path") is not None:
        image = Image.query.filter_by(path=test_input["path"]).first()
        assert image is None

def test_update_image_info_with_valid_data(flask_test_client, auth, user, artist, db, image, json):
    """Test that an image resource can be succesfully updated
    when valid data is sent to the api.
    """
    updated_image_object = {
        "path": "/Users/updateduser/updated_test_project/app/static"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/artists/{artist.id}/images",
        headers=get_headers(token),
        data=json.dumps(updated_image_object)
    )
    assert response.status == "204 NO CONTENT"
    assert response.content_type == "application/json"
    assert response.get_data(as_text=True) == ""

    updated_image = Image.query.filter_by(path=updated_image_object["path"]).first()
    assert updated_image is not None
    assert updated_image.artist_id == artist.id
   
def test_update_image_with_unknown_field_must_fail(flask_test_client, auth, user, json, artist, image):
    """Test that a 400 http status is returned when trying to send
    a field that doesn't exist to the api.
    """
    updated_image_object = {
        "new_field": 1000,
        "path": "/Users/updateduser/updated_test_project/app/static"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/artists/{artist.id}/images",
        headers=get_headers(token),
        data=json.dumps(updated_image_object)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"]["new_field"] == ["Unknown field."]
