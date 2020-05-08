"""This module contains the spider to crawl Time's website."""


from datetime import datetime, timedelta
from scrapy.spiders import CrawlSpider
from scrapy_splash import SplashRequest
from app.performance_scraper.performance_scraper.items import ArtistItem, PerformanceItem
from app.performance_scraper.performance_scraper.venues import time_item


# Time's website uses a Wix widget that uses javascript to display events dynamically
class TimeSpider(CrawlSpider):
    """Spider to crawl Time's website."""

    name = "time"
    start_urls = ["https://www.timerestaurant.net/music-events"]
    lua_script = """
    function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(args.wait))
    return splash:html()   
    end
    """

    def start_requests(self):
        """Send requests to the Splash API."""
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                method="GET",
                endpoint="execute",
                args={"wait": 15, "lua_source": self.lua_script},
            )

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        event_list_link = response.css("#comp-iokgucluiframe").attrib["src"]
        yield SplashRequest(
                url=event_list_link,
                callback=self.parse_event_list,
                method="GET",
                endpoint="execute",
                args={"wait": 15, "lua_source": self.lua_script},
            )
        
    def parse_event_list(self, response):
        """Callback method to parse the event list for information and 
        yield PerformanceItem instances.
        """
        for event in response.css("table.day"):
            artist_item = ArtistItem()
            artist_item["name"] = event.css("div.event-title span::text").get()

            performance_item = PerformanceItem()
            performance_item["title"] = artist_item["name"]
            performance_item["url"] = self.start_urls[0]
            date = event.css("div.when.material-icon.date::text").get()
            start_time, end_time = event.css("div.when.material-icon.time::text").get().split("-")
            performance_item["start_datetime"] = self.format_datetime(date, start_time)
            performance_item["end_datetime"] = self.format_datetime(date, end_time, end=True)

            performance_item["venue"] = dict(time_item)
            performance_item["artist"] = dict(artist_item)
            print(performance_item)
            yield performance_item

    def format_datetime(self, date_string, time_string, end=False):
        """Given a time and date in string form, format the
        date so that it is in the format month/day/year hour:minute.
        """
        datetime_object = datetime.strptime(date_string + " " + time_string, "%A, %B %d, %Y %I:%M%p")
        #Time's events usually end anywhere between midnight and two in the morning. This means that
        #the day attibute will need to be changed to reflect tomorrow's date when calculating the end_datetime
        if end:
            if datetime_object.hour >= 0 and datetime_object.hour <= 2:
                datetime_object = datetime_object + timedelta(days=1)
        return datetime_object.strftime("%m/%d/%Y %H:%M")

