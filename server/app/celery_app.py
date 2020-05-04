"""This module contains the celery app instance."""


from app import init_celery


celery_app = init_celery()


