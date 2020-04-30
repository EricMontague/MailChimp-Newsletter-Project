"""This module contains the spider for scraping the Kimmell Center's website."""


from datetime import datetime, timedelta
from scrapy.spiders import CrawlSpider
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
from performance_scraper.items import PerformanceItem, ArtistItem, ImageItem
from performance_scraper.venues import kimmel_center_item


class KimmelCenterSpider(CrawlSpider):
    """Spider to crawl the Kimmel Center's website."""

    name = "kimmel_center"
    start_urls = ["https://www.kimmelcenter.org/events-and-tickets/#?genre=jazz%20%26%20blues&query="]
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
                method="GET",
                endpoint="execute",
                callback=self.parse,
                args={"wait": 15.0, "lua_source": self.lua_script}
            )


    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        for event in response.css("div.event-content"):
            date = event.css("h3.event-details-date::text").get()
            #A date with a hypen indicates a multi-day performance (e.g. May 12 - May 14)
            #Jazz events usually don't have multi-day performances so I'll skip dates formatted like this
            if "-" not in date:
                time = event.css("p.event-details-time span.ng-binding.ng-scope::text").get()
                start_datetime = self.format_datetime(date, time)
                if start_datetime >= datetime.now() and start_datetime < datetime.now() + timedelta(weeks=4):
                    event_link = event.css("div.event-details a.data-ng-href").attrib["href"]
                    yield SplashRequest(
                        url=event_link,
                        method="GET",
                        endpoint="execute",
                        callback=self.parse_event,
                        args={"wait": 15.0, "lua_source": self.lua_script},
                        cb_kwargs={"start_datetime": start_datetime}
                    )
                else:
                    raise CloseSpider(reason="All events within one month have been processed.")

    def format_datetime(self, date_string, time_string, format="%B %d, %Y %I:%M %p"):
        """Given the date and time as a string, return a
        datetime object.
        """
        return datetime.strptime(date_string + " " + time_string, format)
        
    def parse_event(self, response, start_datetime, format="%m/%d/%Y %H:%M"):
        """Parse the html for a single event page and yield a Performance Item."""
        event_type = response.css("span.pdp-also-more a.cta-link.pdp-also-link::text").get()
        #only want to parse html for jazz events
        if event_type != "[Jazz & Blues]":
            yield {}
        image_item = ImageItem()
        image_item["url"] = response.css("#MainContent_imgBannerBackgroundMobile").attrib["src"]

        artist_item = ArtistItem()
        artist_item["image"] = dict(image_item)
        artist_item["name"] = response.css("h2.pdp-header-title::text").get()

        performance_item = PerformanceItem()
        performance_item["url"] = self.start_urls[0]
        performance_item["title"] = artist_item["name"]
        performance_item["description"] = " ".join(response.css("div.pdp-overview-details div.rich-text div > p::text").getall())
        performance_item["start_datetime"] = start_datetime.strftime(format)
        #The Kimmel Center's events usually last 2 hours
        performance_item["end_datetime"] = (start_datetime + timedelta(hours=2)).strftime(format)

        performance_item["venue"] = dict(kimmel_center_item)
        performance_item["artist"] = dict(artist_item)
        yield performance_item

