"""This module contains the celery app instance."""


from config import BaseConfig
from celery.schedules import crontab
from celery import Celery
from app.scrapy.performance_scraper.tasks import SPIDERS


def init_celery():
    """Return a Celery instance after setting up its configurations."""
    celery = Celery(
        __name__,
        broker=BaseConfig.CELERY_BROKER_URL,
        backend=BaseConfig.CELERY_RESULT_BACKEND
    )
    celery.conf.update(BaseConfig.__dict__)
    celery.conf.beat_schedule = {
        "crawl-every-sunday-morning": {
            "task": "app.scrapy.performance_scraper.tasks.scheduled_crawl",
            "schedule": crontab(hour=9, minute=0, day_of_week=0),
            "args": SPIDERS
        }
    }
    return celery


celery_app = init_celery()


