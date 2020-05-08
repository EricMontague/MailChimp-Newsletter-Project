"""This package contains modules related to Celery."""


from app.celery_app.config import CeleryConfig
from celery import Celery


def init_celery():
    """Return a Celery instance after setting up its configurations."""
    celery = Celery(
        __name__,
        broker=CeleryConfig.CELERY_BROKER_URL,
        backend=CeleryConfig.CELERY_RESULT_BACKEND
    )
    celery.conf.update(CeleryConfig.__dict__)
    return celery


celery_app = init_celery()

