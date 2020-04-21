"""This module contains the spider for scraping Paris Bistro's website."""


from scrapy.spiders import CrawlSpider
from performance_scraper.items import PerformanceItem, ArtistItem, ImageItem
from performance_scraper.venues import paris_bistro_item


class ParisBistroSpider(CrawlSpider):
    """Spider to crawl Paris Bistro's website."""

    name = "paris_bistro"
    start_urls = ["https://parisbistro.net/music/"]

    def parse(self, response):
        """Parse the html for performance information and 
        yield PerformanceItem instances.
        """
        
        main_content = response.xpath("//div[@id='content']")
        for content in main_content.css("div.vc_row.wpb_row.vc_inner.vc_row-fluid"):
            image = content.css("img").attrib["src"]
            date = content.css("h2::text")[0] #need to format this
            title = content.css("h2::text")[1] #need to take cover charge out
            description = content.css("p::text")

    def format_datetime(self):
        pass