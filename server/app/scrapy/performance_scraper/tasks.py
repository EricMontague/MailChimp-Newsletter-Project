"""This module contains celery tasks for running the spiders
programatically."""


from app.celery_app import celery_app
from scrapy.spiderloader import SpiderLoader
from scrapy.exceptions import DropItem, CloseSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


SETTINGS = get_project_settings()
SPIDERS = SpiderLoader(SETTINGS).list()


@celery_app.task(bind=True, throws=(DropItem, CloseSpider))
def start_crawl(spider):
    """Start a crawl using the given spider's name
    passed as a string.
    """
    process = CrawlerProcess(SETTINGS)
    process.crawl(spider)
    process.start()
    self.update_state(
        state="PROGRESS",
        meta={"spider_name": spider}
    )







