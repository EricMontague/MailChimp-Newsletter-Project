"""This module contains the views for executing Scrapy crawls
as Celery tasks.
"""


from flask_restul import Resource
from app.scrapy.performance_scraper.tasks import start_crawl
from celery import group
from http import HTTPStatus


class CrawlTaskAPI:
    """Class with methods for executing and checking the status
    of a single crawl.
    """

    def get(self, task_id):
        """Return the status of the given task based on its id."""
        pass

    def post(self):
        """Execute a single spider crawl as a Celery task."""
        pass



class CrawlTaskListAPI:
    """Class with methods for executing and checking the status
    of a Celery group. Each group contains individual spiders that
    are performing crawls in parallel.
    """

    def get(self, group_id):
        """Return the status of the given group based on the group id.
        Each group contains several spiders crawling in parallel.
        """
        pass

    def post(self):
        """Start a group of spiders that will begin crawling in parallel."""
        pass

    