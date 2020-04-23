"""This module contains the spider to scrape performances from Chris' Jazz Cafe."""


from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ChrisJazzCafeSpider(CrawlSpider):
    """Spider to crawl Chris' Jazz Cafe for performances."""

    name = "chris_jazz_cafe"
    start_urls = ["https://www.chrisjazzcafe.com/calendar"]

    def parse(self, response):
        pass
