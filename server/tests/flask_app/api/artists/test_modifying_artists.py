"""This module contains tests for modifying artist resources."""


from pytest import mark
from flask_app.utils import get_headers
from app.models import Artist


def test_create_new_artist_with_valid_data(flask_test_client, auth, user, json, db):
    """Test that a new artist resource can be succesfully created
    when valid data is sent to the api.
    """
    artist_object = {
        "name": "John Coltrane",
        "bio": "the best artist",
        "website": "http://www.johncoltrane.com"
    }
    expected_fields = {
        "id", "name", "bio", "website", "performances", "image", "_links"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/artists",
        headers=get_headers(token),
        data=json.dumps(artist_object)  
    )
    assert response.status == "201 CREATED"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == expected_fields
    
    assert response.json["id"] == 1 
    assert response.json["name"] == artist_object["name"]
    assert response.json["bio"] == artist_object["bio"]
    assert response.json["website"] == artist_object["website"]
    assert response.json["performances"] == []
    assert response.json["image"] is None
    assert response.json["_links"]["uri"] == "/api/v1/artists/1"
    assert response.json["_links"]["collection"] == "/api/v1/artists"
    

    #Cleanup
    new_artist = Artist.query.get(response.json["id"])
    assert new_artist is not None
    assert new_artist.name == artist_object["name"]
    assert new_artist.bio == artist_object["bio"]
    assert new_artist.website == artist_object["website"]
    
    db.session.delete(new_artist)


@mark.parametrize(
    "test_input, expected",
    [   
        (
            {"name": None, "bio": "new test bio", "website": "http://www.testwebsite.com"},
            {"incorrect_field": "name", "message": ["Field may not be null."]}
        ),
        (
            {"bio": "new test bio", "website": "http://www.testwebsite.com"},
            {"incorrect_field": "name", "message": ["Missing data for required field."]}
        ),
        (
            {"name": "Drake" * 30, "bio": "new test bio", "website": "http://www.testwebsite.com"},
            {"incorrect_field": "name", "message": ["Length must be between 1 and 64."]}
        ),
        (
            {"name": "", "bio": "new test bio", "website": "http://www.testwebsite.com"},
            {"incorrect_field": "name", "message": ["Length must be between 1 and 64."]}
        ),
        (
            {"name": "Drake", "bio": "new test bio", "website": "example.com"},
            {"incorrect_field": "website", "message": ["Not a valid URL."]}
        )
    ]
)
def test_create_new_artist_with_invalid_data_must_fail(flask_test_client, auth, user, json, test_input, expected):
    """Test that a new artist resource cannot be created
    if invalid data is passed to the api.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/artists",
        headers=get_headers(token),
        data=json.dumps(test_input)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"][expected["incorrect_field"]] == expected["message"]

    artist = Artist.query.first()
    assert artist is None


def test_create_new_artist_with_duplicate_name_must_fail(flask_test_client, auth, user, artist, json):
    """Test to ensure that a new artist can't be created
    with a duplicate name.
    """
    artist_object = {
        "name": artist.name,
        "bio": "test bio",
        "website": "http://www.uber.com"
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/artists",
        headers=get_headers(token),
        data=json.dumps(artist_object)
    )

    assert response.status == "409 CONFLICT"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Artist already exists."

    #only the fixture should be in the database
    assert Artist.query.count() == 1


def test_update_artist_info_with_valid_data(flask_test_client, auth, user, db, artist, json):
    """Test that an artist resource can be succesfully updated
    when valid data is sent to the api.
    """
    updated_artist_object = {
        "name": "Miles Davis",
        "bio": artist.bio,
        "website": artist.website
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/artists/{artist.id}",
        headers=get_headers(token),
        data=json.dumps(updated_artist_object)
    )
    assert response.status == "204 NO CONTENT"
    assert response.content_type == "application/json"
    assert response.get_data(as_text=True) == ""

    updated_artist = Artist.query.get(artist.id)
    assert updated_artist is not None
    assert updated_artist.bio is not None
    assert updated_artist.website is not None
    assert updated_artist.name == updated_artist_object["name"]
    assert updated_artist.bio == artist.bio
    assert updated_artist.website == artist.website
    

@mark.parametrize(
    "test_input, expected",
    [
        (
            {"name": "Miles Davis" * 10, "website": "http://www.milesdavis.com"},
            {"incorrect_field": "name", "message": ["Length must be between 1 and 64."]}
        ),
        (
            {"name": "", "website": "http://www.milesdavis.com"},
            {"incorrect_field": "name", "message": ["Length must be between 1 and 64."]}
        ),
        (
            {"bio": "The best bio" * 10, "website": "http://www.milesdavis.com"},
            {"incorrect_field": "name", "message": ["Missing data for required field."]}
        )
    ]
)
def test_update_artist_info_with_invalid_data_must_fail(flask_test_client, auth, user, 
                                                        db, json, test_input, artist, expected):
    """Test that an artist resource cannot be updated
    if invalid data is passed to the api.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/artists/{artist.id}",
        headers=get_headers(token),
        data=json.dumps(test_input)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"][expected["incorrect_field"]] == expected["message"]

    if test_input.get("name") is not None:
        updated_artist = Artist.query.filter_by(name=test_input["name"]).first()
        assert updated_artist is None


@mark.parametrize(
    "test_input, expected",
    [
        (
            {"name": "Miles Davis", "website": "http://www.milesdavis.com"},
            {"message": ["Missing one or more fields."]}
        ),
        (
            {"name": "Miles Davis", "bio": "The best bio"},
            {"message": ["Missing one or more fields."]}
        )
    ]
)
def test_update_artist_info_with_missing_field_must_fail(flask_test_client, auth, user,
                                                        db, json, test_input, artist, expected):
    """Test to ensure that a PUT request cannot be made with any missing fields."""
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/artists/{artist.id}",
        headers=get_headers(token),
        data=json.dumps(test_input)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"]["_schema"] == expected["message"]

    if test_input.get("name") is not None:
        updated_artist = Artist.query.filter_by(name=test_input["name"]).first()
        assert updated_artist is None


def test_update_artist_id_must_fail(flask_test_client, auth, user, json, artist):
    """Test that a artist's id cannot be updated."""
    updated_artist_object = {
        "id": 1000,
        "name": artist.name,
        "bio": artist.bio,
        "website": artist.website
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/artists/{artist.id}",
        headers=get_headers(token),
        data=json.dumps(updated_artist_object)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"]["id"] == ["Unknown field."]


def test_delete_artist(flask_test_client, auth, user, artist, db):
    """Test that an artist resource can be successfully deleted."""
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.delete(
        f"/api/v1/artists/{artist.id}",
        headers=get_headers(token)
    )
    assert response.status == "204 NO CONTENT"
    assert response.content_type == "application/json"
    assert response.get_data(as_text=True) == ""

    artist_object = Artist.query.get(artist.id)
    assert artist_object is None


def test_delete_artist_not_found_must_fail(flask_test_client, auth, user):
    """Test that a 404 error is returned if
    an artist with the given id does not
    exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.delete(
        "/api/v1/artists/100",
        headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Artist could not be found."
