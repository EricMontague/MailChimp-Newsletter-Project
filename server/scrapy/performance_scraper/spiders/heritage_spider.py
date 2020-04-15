"""This module contains a spider to crawl Heritage's website."""


from scrapy.spiders import CrawlSpider, Rule
from performance_scraper.items import PerformanceItem, ArtistItem, VenueItem, ImageItem


class HeritageSpider(CrawlSpider):
    """Spider to crawl Heritage's website."""

    name = "heritage_spider"
    venue = "Heritage"
    street_address = "914 N. 2nd St."
    city = "Philadelphia"
    state = "PA"
    zip_code = "19123"
    start_urls = ["https://heritage.life/events/"]

    def parse(self, response):
        """Parse the response and return PerformanceItem instances."""
        performances = []
        container = response.css("dl.simcal-events-list-container")
        for performance_date, performance_details in zip(
            container.css("dt.simcal-day-label"), container.css("dd.simcal-day")
        ):
            #format of date is Monday, April 13th
            string_date = performance_date.css(".simcal-date-format::text").get()
            for performance in performance_details.css("li.simcal-event"):
                start_time = performance.css(".simcal-event-start::text").get()
                end_time = performance.css(".simcal-event-end::text").get()
                title = performance.css(".simcal-event-title::text").get()
                performances.append((string_date, start_time, end_time, title))
