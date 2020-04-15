# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PerformanceItem(scrapy.Item):
    """Class to represent a performance."""

    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    start_datetime = scrapy.Field()
    end_datetime = scrapy.Field()


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
    

class ImageItem(scrapy.Item):
    """Class to represent an image."""

    filename = scrapy.Field()
