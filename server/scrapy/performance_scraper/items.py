"""This module contains Scrapy Item classes for used throught the project."""


import scrapy


class PerformanceItem(scrapy.Item):
    """Class to represent a performance."""

    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    start_datetime = scrapy.Field()
    end_datetime = scrapy.Field()
    artist = scrapy.Field()
    artist_id = scrapy.Field()
    venue = scrapy.Field()
    venue_id = scrapy.Field()
    image = scrapy.Field()


class VenueItem(scrapy.Item):
    """Class to represent a venue."""

    name = scrapy.Field()
    street_address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()


class ArtistItem(scrapy.Item):
    """Class to represent an artist."""

    name = scrapy.Field()
    bio = scrapy.Field()
    website = scrapy.Field()
    image = scrapy.Field()


class ImageItem(scrapy.Item):
    """Class to represent the image of an artist."""

    url = scrapy.Field()
    path = scrapy.Field()
    
    

#performance item structure
# {
#     "artist": {
#         "name": None,
#         "bio": None,
#         "website": None,
#      },
#     "venue": {
#         "name": None,
#         "street_address": None,
#         "city": None,
#         "state": None,
#         "zip_code": None
#     },
#     "start_datetime": None,
#     "end_datetime": None,
#     "title": None,
#     "description": None,
#     "url": None,
#     "image": {
#          "url": None,
#          "path": None 
#      }
# }
