"""This module contains the spider for scraping the Philadelphia Art Museum's website."""


from datetime import datetime, timedelta
from scrapy.spiders import CrawlSpider
from scrapy_splash import SplashRequest
from performance_scraper.items import PerformanceItem, ArtistItem, ImageItem
from performance_scraper.venues import art_museum_item


class ArtMuseumSpider(CrawlSpider):
    """Spider to crawl the Philadelphia Art Museum's website."""

    name = "art_museum"
    start_urls = ["https://www.philamuseum.org/calendar/view-all/all/performances"]
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
                args={"wait": 15.0, "lua_source": self.lua_script}
            )

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        events = response.css("div.column.scroll-item.is-one-third-tablet.is-full-mobile")
        for event in events:
            if "Friday Nights" in event.css("span.card-title.h4 span::text").get():
                datetimes = event.css("div.card-text.card-subhead span::text").get()
                start_datetime, end_datetime = self.format_datetimes(datetimes)
                if start_datetime >= datetime.now() and start_datetime < datetime.now() + timedelta(months=1):
                    event_link = response.css("a").attrib["src"]
                    yield SplashRequest(
                        url=event_link, 
                        callback=self.parse_event,
                        method="GET",
                        endpoint="execute",
                        args={"wait": 15.0, "lua_source": self.lua_script},
                        cb_kwargs={"start_datetime": start_datetime, "end_datetime": end_datetime}
                    )

    def format_datetimes(self, datetimes):
        """Given start and ending times of an event, return a tuple
        consisting of a start_datetime object and an end_datetime object.
        """ 
        date, times = datetimes.split(", ")
        start_time, end_time = times.split(" - ")
        year = datetime.now().strftime("%Y")
        format = "%B %d %Y %I:%M %p"
        return (
            datetime.strptime(date + " " + year + " " + start_time.replace(".", ""), format),
            datetime.strptime(date + " " + year + " " + end_time.replace(".", ""), format)
        )
        
    def parse_event(self, response, start_datetime, end_datetime):
        """Parse the html for a single event page and yield a Performance Item."""

        image_item = ImageItem()
        image_item["url"] = ""

        artist_item = ArtistItem()
        artist_item["name"] = ""
        artist_item["image"] = dict(image_item)

        performance_item = PerformanceItem()
        performance_item["url"] = self.start_urls[0]
        performance_item["title"] = artist_item["name"]
        performance_item["description"] = ""
        performance_item["start_datetime"] = start_datetime.strftime("%m/%d/%Y %H:%M")
        performance_item["end_datetime"] = end_datetime.strftime("%m/%d/%Y %H:%M")
        performance_item["venue"] = dict(art_museum_item)
        performance_item["artist"] = dict(artist_item)
        yield performance_item
        pass

