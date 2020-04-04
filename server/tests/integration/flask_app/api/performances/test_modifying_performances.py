"""This module contains tests for modifying performance resources."""


from pytest import mark
from datetime import datetime
from flask_app.utils import get_headers
from app.models import Performance


def test_create_new_performance_with_valid_data(
    flask_test_client, auth, user, artist, venue, json, db
):
    """Test that a new performance resource can be succesfully created
    when valid data is sent to the api.
    """
    performance_object = {
        "title": "New test performance",
        "description": "New test performance description.",
        "url": "http://www.testperformance.com",
        "start_datetime": "04/12/2020 10:00",
        "end_datetime": "04/13/2020 10:00",
        "venue_id": venue.id,
        "artist_id": artist.id,
    }
    expected_fields = {
        "id",
        "title",
        "description",
        "url",
        "start_datetime",
        "end_datetime",
        "artist",
        "venue",
        "_links",
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/performances",
        headers=get_headers(token),
        data=json.dumps(performance_object),
    )
    assert response.status == "201 CREATED"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == expected_fields

    assert response.json["id"] == 1
    assert response.json["title"] == performance_object["title"]
    assert response.json["description"] == performance_object["description"]
    assert response.json["url"] == performance_object["url"]
    assert response.json["start_datetime"] == performance_object["start_datetime"]
    assert response.json["end_datetime"] == performance_object["end_datetime"]
    assert response.json["artist"] == f"/api/v1/artists/{artist.id}"
    assert response.json["venue"] == f"/api/v1/venues/{venue.id}"
    assert response.json["_links"]["uri"] == "/api/v1/performances/1"
    assert response.json["_links"]["collection"] == "/api/v1/performances"

    new_performance = Performance.query.get(response.json["id"])
    assert new_performance is not None
    assert new_performance.title == performance_object["title"]
    assert new_performance.description == performance_object["description"]
    assert new_performance.url == performance_object["url"]
    assert (
        new_performance.start_datetime.strftime("%m/%d/%Y %H:%M")
        == performance_object["start_datetime"]
    )
    assert (
        new_performance.end_datetime.strftime("%m/%d/%Y %H:%M") == performance_object["end_datetime"]
    )
    assert new_performance.venue_id == venue.id
    assert new_performance.artist_id == artist.id

    # Cleanup
    db.session.delete(new_performance)


#need to consider putting this in a separate file
@mark.parametrize(
    "test_input, expected",
    [
        (
            {
                "title": "New Test Performance" * 50,
                "description": "foo",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "title", "message": ["Length must be between 1 and 128."]},
        ),
        (
            {
                "title": "",
                "description": "foo",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "title", "message": ["Length must be between 1 and 128."]},
        ),
        (
            {
                "title": "New Test Performance",
                "description": "",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "description", "message": ["Shorter than minimum length 1."]},
        ),
        (
            {
                "title": "New Test Performance",
                "description": "Test description",
                "url": "test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "url", "message": ["Not a valid URL."]},
        ),
        (
            {
                "title": "New Test Performance",
                "description": "Test description",
                "url": "http://www.test.com",
                "start_datetime": "4-12-2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "start_datetime", "message": ["Not a valid datetime."]},
        ),
        (
            {
                "title": "New Test Performance",
                "description": "Test description",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "4-12-2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "end_datetime", "message": ["Not a valid datetime."]},
        )
    ]
)
def test_create_new_performance_with_invalid_data_must_fail(
    flask_test_client, auth, user, json, test_input, expected
):
    """Test that a new performance resource cannot be created
    if invalid data is passed to the api.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/performances", headers=get_headers(token), data=json.dumps(test_input)
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"][expected["incorrect_field"]] == expected["message"]

    performance = Performance.query.first()
    assert performance is None


def test_create_new_performance_with_end_date_before_start_date_must_fail(
    flask_test_client, auth, user, json, artist, venue
):
    """Test that a new performance can't be created if the end date
    is before the start date.
    """
    performance_object = {
        "title": "New test performance",
        "description": "New test performance description.",
        "url": "http://www.testperformance.com",
        "start_datetime": "04/12/2020 10:00",
        "end_datetime": "04/11/2020 10:00",
        "venue_id": venue.id,
        "artist_id": artist.id,
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/performances",
        headers=get_headers(token),
        data=json.dumps(performance_object),
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"]["_schema"] == ["Start date must be before end date."]

    performance = Performance.query.first()
    assert performance is None


def test_create_new_performance_with_end_time_before_start_time_must_fail(
    flask_test_client, auth, user, json, venue, artist
):
    """Test that a new performance can't be created if the end time
    is before the start time.
    """
    performance_object = {
        "title": "New test performance",
        "description": "New test performance description.",
        "url": "http://www.testperformance.com",
        "start_datetime": "04/12/2020 10:00",
        "end_datetime": "04/12/2020 8:00",
        "venue_id": venue.id,
        "artist_id": artist.id,
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.post(
        "/api/v1/performances",
        headers=get_headers(token),
        data=json.dumps(performance_object),
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"]["_schema"] == ["Start time must be before end time."]

    performance = Performance.query.first()
    assert performance is None


def test_update_performance_info_with_valid_data(
    flask_test_client, auth, user, db, performance, json, artist, venue
):
    """Test that a performance resource can be succesfully updated
    when valid data is sent to the api.
    """
    updated_performance_object = {
        "title": "Updated performance title",
        "description": performance.description,
        "url": performance.url,
        "start_datetime": performance.start_datetime.strftime("%m/%d/%Y %H:%M"),
        "end_datetime": performance.end_datetime.strftime("%m/%d/%Y %H:%M"),
        "venue_id": venue.id,
        "artist_id": artist.id,
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/performances/{performance.id}",
        headers=get_headers(token),
        data=json.dumps(updated_performance_object),
    )
    assert response.status == "204 NO CONTENT"
    assert response.content_type == "application/json"
    assert response.get_data(as_text=True) == ""

    updated_performance = Performance.query.get(performance.id)
    assert updated_performance.title == updated_performance_object["title"]
    assert updated_performance.description == updated_performance_object["description"]
    assert updated_performance.url == updated_performance_object["url"]
    assert updated_performance.start_datetime.strftime("%m/%d/%Y %H:%M") == updated_performance_object["start_datetime"]
    assert updated_performance.end_datetime.strftime("%m/%d/%Y %H:%M") == updated_performance_object["end_datetime"]
    assert updated_performance.venue_id == updated_performance_object["venue_id"]
    assert updated_performance.artist_id == updated_performance_object["artist_id"]


#need to consider putting this in a separate file
@mark.parametrize(
    "test_input, expected",
    [
        (
            {
                "title": "New Test Performance" * 50,
                "description": "foo",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "title", "message": ["Length must be between 1 and 128."]},
        ),
        (
            {
                "title": "",
                "description": "foo",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "title", "message": ["Length must be between 1 and 128."]},
        ),
        (
            {
                "title": "New Test Performance",
                "description": "",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "description", "message": ["Shorter than minimum length 1."]},
        ),
        (
            {
                "title": "New Test Performance",
                "description": "Test description",
                "url": "test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "url", "message": ["Not a valid URL."]},
        ),
        (
            {
                "title": "New Test Performance",
                "description": "Test description",
                "url": "http://www.test.com",
                "start_datetime": "4-12-2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "start_datetime", "message": ["Not a valid datetime."]},
        ),
        (
            {
                "title": "New Test Performance",
                "description": "Test description",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "4-12-2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "end_datetime", "message": ["Not a valid datetime."]},
        )
    ]
)
def test_update_performance_info_with_invalid_data_must_fail(
    flask_test_client, auth, user, db, json, test_input, artist, venue, performance, expected
):
    """Test that a performance resource cannot be updated
    if invalid data is passed to the api.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/performances/{performance.id}",
        headers=get_headers(token),
        data=json.dumps(test_input),
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"][expected["incorrect_field"]] == expected["message"]

    if test_input.get("title") is not None:
        updated_performance = Performance.query.filter_by(title=test_input["title"]).first()
        assert updated_performance is None


@mark.parametrize(
    "test_input, expected",
    [
        (
            {
                "description": "foo",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "title", "message": ["Missing data for required field."]},
        ),
        (
            {   
                "title": "Test Title",
                "description": "foo",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "url", "message": ["Missing data for required field."]},
        ),
        (
            {   
                "title": "Test Title",
                "description": "foo",
                "url": "http://www.test.com",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "start_datetime", "message": ["Missing data for required field."]},
        ),
        (
            {   
                "title": "Test Title",
                "description": "foo",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "venue_id": 1,
                "artist_id": 1
            },
            {"incorrect_field": "end_datetime", "message": ["Missing data for required field."]},
        ),
        (
            {   
                "title": "Test Title",
                "description": "foo",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "artist_id": 1
            },
            {"incorrect_field": "venue_id", "message": ["Missing data for required field."]},
        ),
        (
            {   
                "title": "Test Title",
                "description": "foo",
                "url": "http://www.test.com",
                "start_datetime": "04/12/2020 9:00",
                "end_datetime": "04/12/2020 10:00",
                "venue_id": 1
            },
            {"incorrect_field": "artist_id", "message": ["Missing data for required field."]},
        )
    ],
)
def test_update_performance_info_with_missing_field_must_fail(
    flask_test_client, auth, user, db, json, test_input, performance, expected
):
    """Test to ensure that a PUT request cannot be made with any missing fields."""
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/performances/{performance.id}",
        headers=get_headers(token),
        data=json.dumps(test_input),
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"][expected["incorrect_field"]] == expected["message"]

    if test_input.get("title") is not None:
        updated_performance = Performance.query.filter_by(title=test_input["title"]).first()
        assert updated_performance is None


def test_update_performance_id_must_fail(
    flask_test_client, auth, user, json, performance, artist, venue
):
    """Test that a performance's id cannot be updated."""
    updated_performance_object = {
        "id": 1000,
        "title": "New test performance",
        "description": "New test performance description.",
        "url": "http://www.testperformance.com",
        "start_datetime": "04/15/2020 10:00",
        "end_datetime": "04/17/2020 10:00",
        "venue_id": venue.id,
        "artist_id": artist.id,
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.put(
        f"/api/v1/performances/{performance.id}",
        headers=get_headers(token),
        data=json.dumps(updated_performance_object),
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"]["id"] == ["Unknown field."]


def test_delete_performance(flask_test_client, auth, user, performance, db):
    """Test that a performance resource can be successfully deleted."""
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.delete(
        f"/api/v1/performances/{performance.id}", headers=get_headers(token)
    )
    assert response.status == "204 NO CONTENT"
    assert response.content_type == "application/json"
    assert response.get_data(as_text=True) == ""

    performance_object = Performance.query.get(performance.id)
    assert performance_object is None


def test_delete_performance_not_found_must_fail(flask_test_client, auth, user):
    """Test that a 404 error is returned if
    a performance with the given id does not
    exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.delete(
        "/api/v1/performances/100", headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Performance could not be found."
