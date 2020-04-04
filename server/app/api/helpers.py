"""This module contains helper functions for the api blueprint."""


from flask import request, url_for
from datetime import datetime


DEFAULT_PAGE_SIZE = 50
DEFAULT_PAGE_NUMBER = 1


def paginate(tablename, query, schema):
    """Return a paginated collection of resources."""
    page = request.args.get("page", DEFAULT_PAGE_NUMBER, type=int)
    per_page = request.args.get("per_page", DEFAULT_PAGE_SIZE, type=int)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    prev = None
    if pagination.has_prev:
        prev = url_for(request.endpoint, page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for(request.endpoint, page=page + 1)
    return {
        tablename: schema.dumps(pagination.items, many=True),
        "prev": prev,
        "next": next,
        "total": pagination.total
    }


def string_to_date(date_string, format):
    """Given a string date and format, return a 
    corresponding date object.
    """
    try:
        return datetime.strptime(date_string, format).date()
    except ValueError:
        return None
    