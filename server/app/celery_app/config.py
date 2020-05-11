"""This module contains configurations for Celery."""


import os
from celery.schedules import crontab
from app.performance_scraper.performance_scraper.spiders import SPIDERS


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
            "schedule": crontab(hour=16, minute=5, day_of_week=0),
            "args": SPIDERS
        }
    }
    CELERYD_CONCURRENCY = 8
    CELERYD_PREFETCH_MULTIPLIER = 0
    CELERYD_MAX_TASKS_PER_CHILD = 1
    
    

