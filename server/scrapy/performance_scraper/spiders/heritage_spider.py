"""This module contains a spider to crawl Heritage's website."""


from datetime import datetime
from scrapy.spiders import CrawlSpider
from performance_scraper.items import PerformanceItem, ArtistItem
from performance_scraper.venues import heritage_item


class HeritageSpider(CrawlSpider):
    """Spider to crawl Heritage's website."""

    name = "heritage"
    start_urls = ["https://heritage.life/events/"]

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        event_list_container = response.css("dl.simcal-events-list-container")
        for event_date, event_details in zip(
            event_list_container.css("dt.simcal-day-label"), event_list_container.css("dd.simcal-day")
        ):  
            #format of date is Monday, April 13th
            date = event_date.css(".simcal-date-format::text").get()
            for event_detail in event_details.css("li.simcal-event"):
                artist_item = ArtistItem()
                performance_item = PerformanceItem()

                start_time = event_detail.css(".simcal-event-start-time::text").get()
                end_time = event_detail.css(".simcal-event-end-time::text").get()
                title = event_detail.css(".simcal-event-title::text").get()

                performance_item["title"] = title
                performance_item["url"] = self.start_urls[0]
                performance_item["start_datetime"] = self.format_datetime(date, start_time)
                performance_item["end_datetime"] = self.format_datetime(date, end_time)
                performance_item["url"] = self.start_urls[0]
                
                artist_item["name"] = title

                performance_item["artist"] = artist_item
                performance_item["venue"] = heritage_item
                yield performance_item
    
    def format_datetime(self, date_string, time_string):
        """Given a time and date in string form, format the
        date so that it is in the format month/day/year hour:minute.
        """
        month = str(datetime.now().month)
        day = date_string.split()[2][:-2]
        year = str(datetime.now().year)
        #convert time into military time
        time = datetime.strptime(time_string, "%I:%M %p").strftime("%H:%M")
        return month + "/" + day +"/" + year + " " + time


































