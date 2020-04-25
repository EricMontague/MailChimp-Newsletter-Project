"""This module contains the spider to scrape performances from Chris' Jazz Cafe."""


from datetime import datetime, timedelta
from scrapy.spiders import CrawlSpider
from performance_scraper.venues import chris_jazz_item
from performance_scraper.items import ArtistItem, PerformanceItem, ImageItem


class ChrisJazzCafeSpider(CrawlSpider):
    """Spider to crawl Chris' Jazz Cafe for performances."""

    name = "chris_jazz_cafe"
    start_urls = ["https://www.chrisjazzcafe.com/events"]

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        for event in response.css("div.event-list-item"):
            date = event.css("h6.event-date::text").get()
            date = datetime.strptime(date.replace(" ", ""), "%a,%b%d,%Y")
            # will uncomment when running the actual scraper
            # if datetime_object >= datetime.now() + timedelta(days=1) \
            #         and datetime_object <= datetime.now() + timedelta(days=14):
            event_links = event.css("h3.el-header a")
            yield from response.follow_all(
                event_links,
                callback=self.parse_event,
                cb_kwargs={"date": date},
            )

    def parse_event(self, response, date):
        """Parse the individual event's page for information and 
        yield that performance item.
        """
        image_item = ImageItem()
        image_item["url"] = response.css("div.event-image img").attrib["src"]

        artist_item = ArtistItem()
        artist_item["name"] = response.css("h1.event-header::text").get()
        artist_item["bio"] = response.css("#mobile-descr div.custom-content:last-child p::text").get()
        artist_item["image"] = dict(image_item)
        
        performance_item = PerformanceItem()
        performance_item["title"] = artist_item["name"]
        performance_item["description"] = response.css("#mobile-descr div.custom-content:first-child p::text").get()
        start_time = response.css("div.event-divider a:first-child::text").get().replace(" ", "")
        performance_item["start_datetime"] = date.strftime("%m/%d/%Y") + " " + self.convert_to_military_time(start_time)
        end_time = response.css("div.event-divider a:last-child::text").get().replace(" ", "")
        performance_item["end_datetime"] = date.strftime("%m/%d/%Y") + " " + self.convert_to_military_time(end_time)
        performance_item["url"] = response.url

        performance_item["venue"] = dict(chris_jazz_item)
        performance_item["artist"] = dict(artist_item)
        yield performance_item

    def convert_to_military_time(self, time):
        """Convert the given time to military time."""
        return datetime.strptime(time, "%H:%M%p").strftime("%H:%M")


