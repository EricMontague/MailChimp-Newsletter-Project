"""This module contains celery tasks for running the spiders
programatically."""


import traceback
from scrapy.exceptions import DropItem, CloseSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from app.celery_app import celery_app 


SETTINGS = get_project_settings()


@celery_app.task(bind=True, throws=(DropItem, CloseSpider))
def start_crawl(self, spider):
    """Start a crawl using the given spider's name
    passed as a string.
    """
    self.update_state(
        state="PROGRESS",
        meta={"spider_name": spider}
    )
    process = CrawlerProcess(SETTINGS)
    process.crawl(spider)
    process.start()
    


@celery_app.task(throws=(DropItem, CloseSpider))
def scheduled_crawl(spiders):
    """Start the weekly scheduled crawl, using all spiders."""
    process = CrawlerProcess(SETTINGS)
    for spider in spiders:
        process.crawl(spider)
    process.start()
    
