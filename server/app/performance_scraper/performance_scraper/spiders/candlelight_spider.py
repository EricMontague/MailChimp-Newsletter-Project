"""This module contains the spider to scrape performances from The Candlelight Lounge"""


from datetime import datetime
from scrapy.spiders import CrawlSpider
from app.performance_scraper.performance_scraper.items import PerformanceItem, ArtistItem
from app.performance_scraper.performance_scraper.venues import candlelight_item


class CandlelightSpider(CrawlSpider):
    """Spider to crawl Candlelight's website."""

    name = "candlelight"
    set_times = {"start_time": "15:30", "end_time": "19:30"}
    start_urls = ["http://jazztrenton.com/schedule/"]

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        event_container = response.css("div.art-postcontent.clearfix")
        #page is formatted weirdly and there is a single event outside of the main div that
        #holds the rest of the events
        first_event = event_container.css("div:nth-child(4)::text").get()
        event_html = event_container.css("div:last-child").getall()[1]
        event_list = event_html[5:][:-8].split("<br>\n")
        event_list.append(first_event)
        for event in event_list:
            artist_item = ArtistItem()
            performance_item = PerformanceItem()
            date, artist = event.split(",", 1)
            artist_item["name"] = artist

            performance_item["title"] = artist_item["name"]
            performance_item["url"] = self.start_urls[0]
            formatted_date = self.format_date(date)
            performance_item["start_datetime"] = formatted_date + " " + self.set_times["start_time"]
            performance_item["end_datetime"] = formatted_date + " " + self.set_times["end_time"]
            performance_item["artist"] = dict(artist_item)
            performance_item["venue"] = dict(candlelight_item)
            yield performance_item

    def format_date(self, date_string):
        """Format the given date so that it is in the format month/day/year """
        string_month, day = date_string.split()
        month = datetime.strptime(string_month, "%B").strftime("%B")
        year = datetime.now().strftime("%B")
        return month + "/" + day + "/" + year

