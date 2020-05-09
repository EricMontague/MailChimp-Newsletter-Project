"""This module contains the spider for scraping @Exuberance's website."""


import re
from datetime import datetime
from scrapy.spiders import CrawlSpider
from app.performance_scraper.performance_scraper.items import PerformanceItem, ArtistItem, ImageItem
from app.performance_scraper.performance_scraper.venues import exuberance_item


class ExuberanceSpider(CrawlSpider):
    """Spider to crawl @Exuberance's website."""

    name = "exuberance"
    start_urls = ["https://exuberance.typepad.com/"]

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        events = response.css("#beta-inner")
        #filters through the event list to choose only events happening in the future
        for event in events.css("div.entry-author-exuberance.entry-type-post.entry"):
            try:
                artist_name, date_and_time, location = event.css("div.entry-body p:nth-last-of-type(6) span::text").getall()
            except ValueError:
                self.logger.error(
                    (f"The blog post titled: {event.css('h3.entry-header a::text').get()}" 
                    "has a different format than the others and couldn't be parsed.")
                    )
                continue
            start_datetime, end_datetime = self.parse_datetimes(date_and_time)
            if datetime.strptime(start_datetime, "%m/%d/%Y %H:%M") >= datetime.now():
                image_item = ImageItem()
                image_item["url"] = event.css("div.entry-body p:nth-child(2) img").attrib["src"]

                artist_item = ArtistItem()
                artist_item["name"] = artist_name
                artist_item["bio"] = " ".join(event.css("div.entry-body p:nth-child(3) span::text").getall())
                artist_item["image"] = dict(image_item)

                performance_item = PerformanceItem()
                performance_item["title"] = artist_item["name"]
                performance_item["url"] = self.start_urls[0]
                performance_item["start_datetime"] = start_datetime
                performance_item["end_datetime"] = end_datetime
                performance_item["artist"] = dict(artist_item)
                performance_item["venue"] = dict(exuberance_item)
                yield performance_item
        
    def parse_datetimes(self, datetime_string):
        """Extract the start and end datetimes from the given datetime_string and return
        them as a tuple.
        """

        datetime_string = "".join(datetime_string.lower().split())
        start_time, end_time, num_day = re.findall(r"\d{1,2}:?\d{0,2}", datetime_string)
        period = self.parse_time_period(datetime_string)
        formatted_start_time = self.format_time(start_time, period)
        formatted_end_time = self.format_time(end_time, period)
        formatted_start_time = self.adjust_start_time(formatted_start_time, formatted_end_time)

        month = self.parse_month(datetime_string)
        year = str(datetime.now().year)
        return (
            month + "/" + num_day + "/" + year + " " + formatted_start_time, 
            month + "/" + num_day + "/" + year + " " + formatted_end_time
            )

    def parse_time_period(self, datetime_string):
        """Find and return the time period in the datetime string."""
        #get 'am' or 'pm'
        period = ""
        for time_period in ["am", "pm"]:
            index = datetime_string.find(time_period)
            if index != -1:
                period += datetime_string[index: index + 2]
        return period

    def parse_month(self, datetime_string):
        """Find and return the month as a number from the string."""
        months = [
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december"
        ]
        num_month = ""
        for month in months:
            index = datetime_string.find(month)
            if index != - 1:
                num_month += datetime.strptime(month, "%B").strftime("%m")
        return num_month

    def format_time(self, time_string, period):
        """Return the time formatted in the following format - hours:minutes.
        If the time is past noon, it will also be converted to military time.
        """
        if ":" not in time_string:
            time = datetime.strptime(time_string + " " + period, "%I %p").strftime("%H:%M")
        else:
            time = datetime.strptime(time_string + " " + period, "%I:%M %p").strftime("%H:%M")
        return time
    
    def adjust_start_time(self, start_time, end_time):
        """Adjust the start time it was incorrectly set to be after the end time. This may
        happen due to the website not specifying whether the start time is in the morning or
        the afternoon.
        """
        if datetime.strptime(start_time, "%H:%M") > datetime.strptime(end_time, "%H:%M"):
            hours, minutes = start_time.split(":")
            start_time = str(int(hours) - 12) + ":" + minutes
        return start_time

        

    