"""This module contains a Scrapy pipeline class for sending data to the Flask API."""


from performance_scraper.api_client import FlaskAPIClient
from performance_scraper.auth import AuthManager


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
            email=crawler.settings.get("SCRAPY_EMAIL")
        )
        token = AuthManager.retrieve_token()
        api_client = FlaskAPIClient(token=token, auth_manager=auth_manager)
        return cls(api_client=api_client)

    def process_item(self, performance_item, spider):
        """Send scraped data to the Flask API to be stored."""

        #separate venue from performance_item
        #separate artist from performance_item

        #make POST request to create a venue. Method should return the venue resource
        #if that fails because it already exists, make GET request to retrieve it by name

        #make POST request to create an artist, method should return the artist resource
        #If that fails because it already exists, make a GET request to retrieve by name

        #Check if an image is included in the artist dictionary
        #if it is, send a PUT request to replace/create the image. Method returns nothing

        #update perofmrnace_item dictionary with venue_id and artist_id
        #make POST request to create a new performance. Method should return a performance resource

        #return item as per Scrapy's requirements

        venue_item = performance_item.pop("venue")
        artist_item = performance_item.pop("artist")
        venue_resource = self.client.post(venue_item, "venues")
        artist_resource = self.client.post(artist_item, "artists")
        if artist.get("image") is not None:
            self.client.put(artist["image"], f"artists/{artist_id}/images", artist_id=artist_id)
        performance_item["venue_id"] = venue_id
        performance_item["artist_id"] = artist_id
        self.client.post(performance_item, "performances")
        return item

        

