"""This module contains the spider to scrape performances from Chris' Jazz Cafe."""


from datetime import datetime, timedelta
from scrapy.spiders import CrawlSpider
from scrapy import Request
from app.performance_scraper.performance_scraper.venues import chris_jazz_item
from app.performance_scraper.performance_scraper.items import ArtistItem, PerformanceItem, ImageItem


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
            event_id = event.css("h3.el-header a").attrib["href"].split("/")[2]
            yield Request(
                response.url + "/" + event_id,
                callback=self.parse_event,
                cb_kwargs={"date": date}
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
        performance_item["start_datetime"] = self.format_datetime(date, start_time)
        end_time = response.css("div.event-divider a:last-child::text").get().replace(" ", "")
        performance_item["end_datetime"] = self.format_datetime(date, end_time, end=True)
        performance_item["url"] = response.url

        performance_item["venue"] = dict(chris_jazz_item)
        performance_item["artist"] = dict(artist_item)
        yield performance_item

    def format_datetime(self, datetime_object, time_string, end=False):
        """Given a time in string form and a datetime object, format the
        date so that it is in the format month/day/year hour:minute.
        """
        time_object = datetime.strptime(time_string, "%I:%M%p").time()
        final_datetime = datetime.combine(datetime_object.date(), time_object)
        #Chris' website gives starting and ending set times instead of starting and ending event times
        if end:
            #If the second set starts at 10pm, then it will usually end at Midnight
            if final_datetime.hour == 22:
                final_datetime = final_datetime + timedelta(hours=2)
            #if the second set starts at 11:30pm, then it will usually end at 2am
            elif final_datetime.hour == 23 and final_datetime.minutes == 30:
                final_datetime = final_datetime + timedelta(hours=2, minutes=30)
        return final_datetime.strftime("%m/%d/%Y %H:%M")


