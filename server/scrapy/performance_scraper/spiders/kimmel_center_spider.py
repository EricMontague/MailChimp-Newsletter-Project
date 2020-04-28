"""This module contains the spider for scraping the Kimmell Center's website."""


from datetime import datetime
from scrapy.spiders import CrawlSpider
from performance_scraper.items import PerformanceItem, ArtistItem, ImageItem
from performance_scraper.venues import kimmel_center_item


class KimmelCenterSpider(CrawlSpider):
    """Spider to crawl the Kimmel Center's website."""

    name = "kimmel_center"
    start_urls = ["https://www.kimmelcenter.org/events-and-tickets/#?genre=jazz%20%26%20blues&query="]

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        pass
