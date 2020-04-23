"""This module contains the spider to crawl Time's website."""


from scrapy.spiders import CrawlSpider
from performance_scraper.items import ArtistItem, PerformanceItem, ImageItem
from performance_scraper.venues import time_item


class TimeSpider(CrawlSpider):
    """Spider to crawl Time's website."""

    name = "time"
    start_urls = ["https://www.timerestaurant.net/music-events"]

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        #Time's website uses a Wix widget to display events. This extracts the link of the
        #wigget, which then leads to the actual list of events
        event_list_source = response.xpath("//iframe[@id='comp-iokgucluiframe']/@data-src").get()
        yield from response.follow(event_list_source, callback=self.parse_event_list)
        
    def parse_event_list(self, response):
        """Callback method to parse the event list for information and 
        yield PerformanceItem instances.
        """
        pass
