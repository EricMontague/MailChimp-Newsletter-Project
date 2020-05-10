"""This module contains the spider for scraping Paris Bistro's website."""


from datetime import datetime, date
from scrapy.spiders import CrawlSpider
from app.performance_scraper.performance_scraper.items import PerformanceItem, ArtistItem, ImageItem
from app.performance_scraper.performance_scraper.venues import paris_bistro_item


class ParisBistroSpider(CrawlSpider):
    """Spider to crawl Paris Bistro's website."""

    name = "paris_bistro"
    start_urls = ["https://parisbistro.net/music/"]
    set_times = {
        "wednesday": {"start_time": "18:30", "end_time": "22:00"}, 
        "thursday": {"start_time": "19:00", "end_time": "23:00"}, 
        "friday": {"start_time": "19:00", "end_time": "23:00"}, 
        "saturday": {"start_time": "19:00", "end_time": "23:00"}, 
        "sunday": {"start_time": "19:00", "end_time": "23:00"}, 
    }

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        event_list = response.xpath("//div[@id='content']")
        for event in event_list.css("div.vc_row.wpb_row.vc_inner.vc_row-fluid"):
            image_item = ImageItem()
            image_item["url"] = event.css("img").attrib["src"]
            
            artist_item = ArtistItem()
            #artist's name is usually in the title, will clean this up on the backend later
            title = self.format_title(event.css("h2::text").getall()[1])
            artist_item["name"] = title
            artist_item["image"] = dict(image_item)

            #format of date is Wednesay, April 12
            date = event.css("h2::text").getall()[0]
            word_day = self.parse_day_as_string(date)
            
            performance_item = PerformanceItem()
            formatted_date = self.format_date(date)
            performance_item["start_datetime"] = formatted_date + " " + self.set_times[word_day]["start_time"]
            performance_item["end_datetime"] = formatted_date + " " + self.set_times[word_day]["end_time"]
            performance_item["title"] = title
            performance_item["description"] = event.css("p::text").get()
            performance_item["url"] = self.start_urls[0]
            performance_item["artist"] = dict(artist_item)
            performance_item["venue"] = dict(paris_bistro_item)
            yield performance_item

    def format_date(self, date_string):
        """Format the given date so that it is in the format month/day/year """
        split_date = date_string.split()
        month = datetime.strptime(split_date[-2], "%B").strftime("%m")
        number_day = split_date[-1] #numeric day. e.g. 13
        year = datetime.now().strftime("%Y")
        return month + "/" + number_day + "/" + year

    def format_title(self, title):
        """Remove the cover charge from the title and return the newly
        formatted title.
        """
        #need to take cover charge out of title string
        return title[:-6]

    def parse_day_as_string(self, date_string):
        """Given a date, return the day as a string. Normally this wouldn't be needed,
        as the day is already in the string, but Paris Bistro sometimes likes to hold special
        events (e.g. Easter Brunch) which will lead to the day being left out of the date.
        """
        split_date = date_string.split()
        month = split_date[-2]
        number_day = split_date[-1] #numeric day. e.g. 13
        year = datetime.now().strftime("%Y")
        datetime_object = datetime.strptime(month + " " + number_day + ", " + year, "%B %d, %Y")
        return datetime_object.strftime("%A").lower()



        
