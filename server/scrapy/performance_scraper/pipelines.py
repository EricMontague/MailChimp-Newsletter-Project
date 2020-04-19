"""This module contains a Scrapy pipeline class for sending data to the Flask API."""


from http import HTTPStatus
from scrapy.exceptions import CloseSpider
from performance_scraper.flask_api.api_client import FlaskAPIClient
from performance_scraper.flask_api.auth import AuthManager
from performance_scraper.flask_api.exceptions import FlaskAPIException


class APIPipeline(object):
    """Class to send data to the Flask API."""

    def __init__(self, api_client):
        self._api_client = api_client

    @classmethod
    def from_crawler(cls, crawler):
        """Return a new APIPipeline instance."""
        auth_manager = AuthManager(
            username=crawler.settings.get("SCRAPY_USERNAME"),
            password=crawler.settings.get("SCRAPY_PASSWORD"),
            email=crawler.settings.get("SCRAPY_EMAIL"),
            cache_path=crawler.settings.get("TOKEN_FILE_PATH"),
        )
        token = auth_manager.get_cached_token()
        api_client = FlaskAPIClient(token=token, auth_manager=auth_manager)
        return cls(api_client=api_client)

    def process_item(self, performance_item, spider):
        """Send scraped data to the Flask API to be stored."""
        venue_item = performance_item.pop("venue")
        artist_item = performance_item.pop("artist")

        # attempt to get venue resource from API. If it doesn't exist, create it
        venue_resource = self.retrieve_venue_info(dict(venue_item))
        if venue_resource is None:
            venue_resource = self.store_venue_info(dict(venue_item))

        # attempt to get artist resource  from API. If it doesn't exist, create it
        artist_resource = self.retrieve_artist_info(dict(artist_item))
        if artist_resource is None:
            artist_resource = self.store_artist_info(dict(artist_item))

        # update artist's image
        if artist_item.get("image") is not None:
            self.store_artist_image(artist_resource["id"], dict(artist_item))
        # update performance item to include venue and artist id's that will
        # need to be sent in the payload to the API
        performance_item["venue_id"] = venue_resource["id"]
        performance_item["artist_id"] = artist_resource["id"]
        self.store_performance_info(dict(performance_item))
        return performance_item

    def retrieve_venue_info(self, venue_item):
        """Return a venue resource by making a call to the Flask API."""
        try:
            venue_resource = self._api_client.get_venue_by_name(venue_item["name"])
        except FlaskAPIException as api_exception:
            if api_exception.http_status == HTTPStatus.NOT_FOUND:
                venue_resource = None
            else:
                raise CloseSpider(
                    reason=api_exception.message
                )
        return venue_resource

    def store_venue_info(self, venue_item):
        """Store the venue's information by making a call to the Flask API."""
        return self._api_client.create_venue(venue_item)

    def retrieve_artist_info(self, artist_item):
        """Return an artist resource by making a call to the Flask API."""
        try:
            artist_resource = self._api_client.get_artist_by_name(artist_item["name"])
        except FlaskAPIException as api_exception:
            if api_exception.http_status == HTTPStatus.NOT_FOUND:
                artist_resource = None
            else:
                raise CloseSpider(
                    reason=api_exception.message
                )
        return artist_resource

    def store_artist_info(self, artist_item):
        """Store the artist's information by making a call to the Flask API."""
        # Create artist resource. Returns None if artist already exists
        return self._api_client.create_artist(artist_item)

    def store_artist_image(self, artist_id, artist_item):
        """Store the artist's image by making a call to the Flask API."""
        # attempt to update artist's image if one was found on the scraped website
        self._api_client.update_artist_image(artist_id, artist_item["image"])

    def store_performance_info(self, performance_item):
        """Store the performance information by making a call to the Flask API."""
        self._api_client.create_performance(performance_item)

