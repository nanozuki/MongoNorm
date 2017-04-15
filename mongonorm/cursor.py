from functools import wraps
from pymongo.cursor import Cursor as OrigCursor


class Cursor(object):
    @classmethod
    def mk_list(cls, collection, orig_cursor_list):
        return [cls(collection, orig_cursor)
                for orig_cursor in orig_cursor_list]

    def __init__(self, collection, orig_cursor):
        self.collection = collection
        self.orig_cursor = orig_cursor

    def decorate_method(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            rtn = f(*args, **kwargs)
            if isinstance(rtn, OrigCursor):
                return Cursor(self.collection, rtn)
            return rtn
        return decorated_function

    def __getattr__(self, name):
        rtn = getattr(self.orig_cursor, name)
        if isinstance(rtn, dict):
            return self.collection._boxing(rtn)
        elif callable(rtn):
            return self.decorate_method(rtn)
        return rtn

    def __getitem__(self, index):
        rtn = self.orig_cursor.__getitem__(index)
        if isinstance(rtn, dict):
            return self.collection._boxing(rtn)
        elif isinstance(rtn, OrigCursor):
            return Cursor(self.collection, rtn)
        elif callable(rtn):
            return self.decorate_method(rtn)
        return rtn

    def __iter__(self):
        return self

    def next(self):
        rtn = self.orig_cursor.next()
        if isinstance(rtn, dict):
            return self.collection._boxing(rtn)
        return rtn

    __next__ = next
