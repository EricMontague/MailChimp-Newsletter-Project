"""This module contains the views for executing Scrapy crawls
as Celery tasks.
"""


from flask import request, url_for
from flask_restful import Resource
from app.scrapy.performance_scraper.tasks import start_crawl
# from app.scrapy.performance_scraper import SPIDERS
from celery import group
from http import HTTPStatus


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


SPIDER_NAMES = set(SPIDERS)


class CrawlTaskAPI(Resource):
    """Class for executing a single Scrapy crawl."""

    def post(self):
        """Execute a single spider crawl as a Celery task."""
        json_data = request.get_json()
        if json_data is None:
            return {"message": "Request missing a JSON body."}, HTTPStatus.BAD_REQUEST
        if "spider" not in json_data:
            return {"message": "Missing parameter - 'spider'"}, HTTPStatus.BAD_REQUEST
        if not isinstance(json_data["spider"], str):
            return (
                {
                    "message": f"Parameter must be a string, not {type(json_data['spider'])}"
                },
                HTTPStatus.BAD_REQUEST,
            )
        if not json_data["spider"]: 
            return {"message": "An empty string is not valid input."}, HTTPStatus.BAD_REQUEST
        spider_name = json_data["spider"].lower().replace(" ", "_") #format spider
        if spider_name not in SPIDER_NAMES:
            return {
                "message": f"Crawl was not started due to an invalid spider being provided.",
                "invalid_spider": spider_name
            }, HTTPStatus.BAD_REQUEST
        async_result = start_crawl.delay(spider_name)
        response = {}
        response["message"] = "Single crawl started."
        response["uri"] = url_for("api.crawl_status", task_id=async_result.id)
        response["task_info"] = {
            "status": async_result.status,
            "spider_name": spider_name
        }
        return response, HTTPStatus.ACCEPTED


class CrawlTaskStatusAPI(Resource):
    """Class for checking the status of a single Scrapy crawl."""

    def get(self, task_id):
        """Return the status of the given task based on its id."""
        #returns an AsyncResult object, but naming the variable 'task' makes this more readable
        task = start_crawl.AsyncResult(task_id)
        response = {"status": task.status}
        if task.status == "SUCCESS":
            response["result"] = task.info
        elif task.status == "FAILURE":
            response["errors"] = str(task.info)
        return response, HTTPStatus.OK


class CrawlGroupAPI(Resource):
    """Class with methods for executing multiple crawls at once using Celery's 
    group function. Each group contains individual spiders that are performing run in parallel.
    """

    def post(self):
        """Start a group of spiders that will begin crawling in parallel."""
        json_data = request.get_json()
        if json_data is None:
            return {"message": "Request missing a JSON body."}, HTTPStatus.BAD_REQUEST
        if "spiders" not in json_data:
            return {"message": "Missing parameter - 'spiders'"}, HTTPStatus.BAD_REQUEST
        if not isinstance(json_data["spiders"], list):
            return (
                {
                    "message": f"Parameter must be a list, not {type(json_data['spiders'])}"
                },
                HTTPStatus.BAD_REQUEST,
            )
        if not json_data["spiders"]:
            return {"message": "List is empty."}, HTTPStatus.BAD_REQUEST
        if len(json_data["spiders"]) == 1:
            return {
                "message": "This endpoint is to be used to execute group crawls."
                + f"Please use the following endpoint for single crawls - {url_for('api.crawl')}."
                }, HTTPStatus.BAD_REQUEST
        invalid_spiders = []
        valid_spiders = []
        for spider in json_data["spiders"]:
            spider_name = spider.lower().replace(" ", "_") #format user input
            if spider_name not in SPIDER_NAMES:
                invalid_spiders.append(spider_name)
            else:
                valid_spiders.append(spider_name)
        if not valid_spiders:
            return {
                "message": "Group crawl was not started due to no valid spiders being provided.", 
                "invalid spiders": invalid_spiders
            }, HTTPStatus.BAD_REQUEST
        crawl_group = group(
            [start_crawl.signature(args=(spider,)) for spider in valid_spiders]
        )
        group_result = crawl_group()
        response = {}
        response["message"] = "Group crawl started."
        response["num_spiders_executed"] = len(valid_spiders)
        response["invalid_spiders"] = invalid_spiders
        response["tasks"] = [
            {
                "status": result.status,
                "spider_name": result.info.get("spider_name"),
                "uri": url_for("api.crawl_status", task_id=result.id),
            }
            for result in group_result.results
        ]
        return response, HTTPStatus.ACCEPTED


