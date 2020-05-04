"""This module contains celery tasks for running the spiders
programatically."""


from app.celery_app import celery_app
from scrapy.exceptions import DropItem, CloseSpider
from scrapy.crawler import CrawlRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor


@celery_app.task(bind=True, throws=(DropItem, CloseSpider))
def start_crawl(spider):
    """Start a crawl using the given spider's name
    passed as a string.
    """
    pass





