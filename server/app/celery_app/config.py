"""This module contains configurations for Celery."""


import os
from celery.schedules import crontab
# from app.scrapy.performance_scraper import SPIDERS

# hard coded until I can find a way to dynamically retrieve these
SPIDERS = [
    'candlelight', 
    'chris_jazz_cafe', 
    'exuberance', 
    'heritage', 
    'kimmel_center',
    'paris_bistro', 
    'art_museum', 
    'time'
]


class CeleryConfig:
    """Class that holds configurations for the Celery instance."""

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
    CELERY_RESULTS_EXPIRE = 60 * 60 * 24 * 2, #two days
    CELERY_TIMEZONE = "US/Eastern"
    CELERY_INCLUDE =  ["app.performance_scraper.performance_scraper.tasks"]
    CELERYBEAT_SCHEDULE = {
        "crawl-every-sunday-morning": {
            "task": "app.performance_scraper.performance_scraper.tasks.scheduled_crawl",
            "schedule": crontab(hour=9, minute=0, day_of_week=0),
            "args": SPIDERS
        }
    }
    CELERY_PREFETCH_MULTIPLIER = 8
    

