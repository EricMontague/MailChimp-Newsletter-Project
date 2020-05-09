"""This module contains celery tasks for running the spiders
programatically."""


import traceback
from scrapy.exceptions import DropItem, CloseSpider
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from app.celery_app import celery_app 
from celery.exceptions import Ignore
from celery import states


configure_logging()
SETTINGS = get_project_settings()


@celery_app.task(bind=True, throws=(DropItem, CloseSpider))
def start_crawl(self, spider):
    """Start a crawl using the given spider's name
    passed as a string.
    """
    self.update_state(
        state="PROGRESS",
        meta={"spider": spider}
    )
    try:
        runner = CrawlerRunner(SETTINGS)
        defferred = runner.crawl(spider)
        defferred.addBoth(lambda x: reactor.stop())
        reactor.run()
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                "exc_type": type(ex).__name__,
                "exc_message": " ".join(traceback.format_exc().split('\n')),
                "spider": spider
            })
        raise Ignore()
    # process = CrawlerProcess(SETTINGS)
    # process.crawl(spider)
    # process.start()
    


@celery_app.task(throws=(DropItem, CloseSpider))
def scheduled_crawl(spiders):
    """Start the weekly scheduled crawl, using all spiders."""
    process = CrawlerProcess(SETTINGS)
    for spider in spiders:
        process.crawl(spider)
    process.start()
    
