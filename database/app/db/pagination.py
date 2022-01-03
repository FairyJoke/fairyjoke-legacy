# from https://github.com/wizeline/sqlalchemy-pagination
# MIT Licensed

import math


class Page(object):
    def __init__(self, items, page, page_size, total):
        self.items = items
        self.prev_page = None
        self.next_page = None
        self.has_prev = page > 1
        if self.has_prev:
            self.prev_page = page - 1
        prev_items = (page - 1) * page_size
        self.has_next = prev_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1
        self.total = total
        self.pages = int(math.ceil(total / float(page_size)))
        self.page = page


def paginate(query, page=1, page_size=40):
    if page <= 0:
        raise AttributeError('page needs to be >= 1')
    if page_size <= 0:
        raise AttributeError('page_size needs to be >= 1')
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    # We remove the ordering of the query since it doesn't matter for getting a count and
    # might have performance implications as discussed on this Flask-SqlAlchemy issue
    # https://github.com/mitsuhiko/flask-sqlalchemy/issues/100
    total = query.order_by(None).count()
    return Page(items, page, page_size, total)
