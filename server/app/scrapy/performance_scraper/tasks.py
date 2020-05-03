from celery import Celery




@app.task(throws=(DropItem, CloseSpider))
def start_crawl(*args, **kwargs):
    pass

