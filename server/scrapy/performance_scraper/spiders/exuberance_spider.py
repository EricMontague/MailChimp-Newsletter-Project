"""This module contains the spider for scraping @Exuberance's website."""


from scrapy.spiders import CrawlSpider
from performance_scraper.items import PerformanceItem, ArtistItem, ImageItem
from performance_scraper.venues import exuberance_item


class ExuberanceSpider(CrawlSpider):
    """Spider to crawl @Exuberance's website."""

    name = "exuberance"
    start_urls = ["https://exuberance.typepad.com/"]

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        pass

    def format_date(self, date_string):
        """Format the given date so that it is in the format month/day/year """
        pass

    