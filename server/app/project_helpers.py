"""This module contains helper functions to be used across the project."""


from flask import request, url_for, current_app


def paginate(tablename, query, schema):
    """Return a paginated collection of resources."""
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get(
        "per_page", current_app.config["DEFAULT_RESOURCES_PER_PAGE"], type=int
    )
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

    