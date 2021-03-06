"""This module contains tests for sending GET requests to the performances subcollection.
The tests are basically the same as test_getting_performances_info.py, except the endpoint
is different.
"""


from pytest import mark
from flask_app.utils import get_headers


def test_getting_list_of_artist_performances_by_authorized_user(
    flask_test_client, json, auth, user, artist, performance
):
    """Test to ensure that a list of performance resources can be
    successfully retrieved.
    """
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
    response = flask_test_client.get(
        f"/api/v1/artists/{artist.id}/performances", headers=get_headers(token)
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == {"performances", "prev", "next", "total"}
    assert isinstance(json.loads(response.json["performances"]), list)
    assert set(json.loads(response.json["performances"])[0].keys()) == expected_fields
    assert response.json["total"] == 1
    assert response.json["prev"] is None
    assert response.json["next"] is None
    assert json.loads(response.json["performances"])[0]["id"] == performance.id
    assert json.loads(response.json["performances"])[0]["title"] == performance.title
    assert (
        json.loads(response.json["performances"])[0]["description"]
        == performance.description
    )
    assert json.loads(response.json["performances"])[0]["url"] == performance.url
    assert (
        json.loads(response.json["performances"])[0]["start_datetime"]
        == performance.start_datetime.strftime("%m/%d/%Y %H:%M")
    )
    assert (
        json.loads(response.json["performances"])[0]["end_datetime"]
        == performance.end_datetime.strftime("%m/%d/%Y %H:%M")
    )
    assert (
        json.loads(response.json["performances"])[0]["venue"]
        == f"/api/v1/venues/{performance.venue.id}"
    )
    assert (
        json.loads(response.json["performances"])[0]["artist"]
        == f"/api/v1/artists/{performance.artist.id}"
    )
    assert (
        json.loads(response.json["performances"])[0]["_links"]["uri"]
        == f"/api/v1/performances/{performance.id}"
    )
    assert (
        json.loads(response.json["performances"])[0]["_links"]["collection"]
        == "/api/v1/performances"
    )


def test_filtering_list_of_artist_performances_by_date(
    flask_test_client, artist, performance, auth, user, json
):
    """Test to ensure that a list performances can be retrieved by starting and ending dates."""
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
    dates = {
        "start_date": performance.start_datetime.strftime("%m/%d/%Y"),
        "end_date": performance.end_datetime.strftime("%m/%d/%Y"),
    }
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/artists/{artist.id}/performances",
        headers=get_headers(token),
        query_string=dates,
    )
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
    assert set(response.json.keys()) == {"performances", "prev", "next", "total"}
    assert isinstance(json.loads(response.json["performances"]), list)
    assert set(json.loads(response.json["performances"])[0].keys()) == expected_fields
    assert response.json["total"] == 1
    assert response.json["prev"] is None
    assert response.json["next"] is None
    assert json.loads(response.json["performances"])[0]["id"] == performance.id
    assert json.loads(response.json["performances"])[0]["title"] == performance.title
    assert (
        json.loads(response.json["performances"])[0]["description"]
        == performance.description
    )
    assert json.loads(response.json["performances"])[0]["url"] == performance.url
    assert (
        json.loads(response.json["performances"])[0]["start_datetime"]
        == performance.start_datetime.strftime("%m/%d/%Y %H:%M")
    )
    assert (
        json.loads(response.json["performances"])[0]["end_datetime"]
        == performance.end_datetime.strftime("%m/%d/%Y %H:%M")
    )
    assert (
        json.loads(response.json["performances"])[0]["venue"]
        == f"/api/v1/venues/{performance.venue.id}"
    )
    assert (
        json.loads(response.json["performances"])[0]["artist"]
        == f"/api/v1/artists/{performance.artist.id}"
    )
    assert (
        json.loads(response.json["performances"])[0]["_links"]["uri"]
        == f"/api/v1/performances/{performance.id}"
    )
    assert (
        json.loads(response.json["performances"])[0]["_links"]["collection"]
        == "/api/v1/performances"
    )


@mark.parametrize(
    "test_input, expected",
    [
        (
            {"start_date": "4/12/2020"},
            {"message": "Please provide both a start and an end date."},
        ),
        (
            {"end_date": "4/12/2020"},
            {"message": "Please provide both a start and an end date."},
        ),
    ],
)
def test_filtering_list_of_artist_performances_by_date_missing_query_parameters_must_fail(
    flask_test_client, artist, auth, user, test_input, expected
):
    """Test that the appropriate errors are returned if incorrect query string parameters are passed
    to the api in an attempt to retrieve performances by date.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/artists/{artist.id}/performances",
        headers=get_headers(token),
        query_string=test_input,
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert response.json["message"] == expected["message"]


@mark.parametrize(
    "test_input, expected",
    [
        (
            {"start_date": "4-12-2020", "end_date": "4/14/2020"},
            {
                "incorrect_parameter": "start_date",
                "message": "Incorrectly formatted date.",
            },
        ),
        (
            {"start_date": "4/12/2020", "end_date": "4-14-2020"},
            {
                "incorrect_parameter": "end_date",
                "message": "Incorrectly formatted date.",
            },
        ),
    ],
)
def test_filtering_list_of_artist_performances_by_date_incorrectly_formatted_dates_must_fail(
    flask_test_client, artist, auth, user, test_input, expected
):
    """Test that the appropriate errors are returned if incorrectly formatted dates are passed
    to the api in an attempt to retrieve performances by date.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/artists/{artist.id}/performances",
        headers=get_headers(token),
        query_string=test_input,
    )
    assert response.status == "400 BAD REQUEST"
    assert response.content_type == "application/json"
    assert (
        response.json["message"][expected["incorrect_parameter"]] == expected["message"]
    )


def test_getting_list_of_artist_performances_without_token_must_fail(
    flask_test_client, artist
):
    """Test to ensure that an unauthorized user (no token) cannot get
    performance resources
    """
    response = flask_test_client.get(
        f"/api/v1/artists/{artist.id}/performances", headers=get_headers()  # no token
    )
    assert response.status == "401 UNAUTHORIZED"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Access token is invalid or expired."


def test_artist_not_found(flask_test_client, auth, user):
    """Test to ensure that a 404 response is returned
    if a artist resource does not exist.
    """
    token = auth.register(user.username, "password", user.email)
    response = flask_test_client.get(
        f"/api/v1/artists/100/performances", headers=get_headers(token)
    )
    assert response.status == "404 NOT FOUND"
    assert response.content_type == "application/json"
    assert response.json["message"] == "Artist could not be found."
