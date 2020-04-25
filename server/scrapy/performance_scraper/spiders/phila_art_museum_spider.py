"""This module contains the spider for scraping the Philadelphia Art Museum's website."""


from datetime import datetime
from scrapy.spiders import CrawlSpider
from performance_scraper.items import PerformanceItem, ArtistItem, ImageItem
from performance_scraper.venues import art_museum_item


class ArtMuseumSpider(CrawlSpider):
    """Spider to crawl the Philadelphia Art Museum's website."""

    name = "art_museum"
    start_urls = ["https://www.philamuseum.org/calendar/view-all/all/performances"]

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        events = response.css("div.column.scroll-item.is-one-third-tablet.is-full-mobile")
        for event in events:
            if "Friday Nights" in event.css("span.card-title.h4 span::text").get():
                datetimes = event.css("div.card-text.card-subhead span::text").get()
                start_datetime, end_datetime = self.format_datetimes(datetimes)


    def format_datetime(self, datetime_string):
        pass

