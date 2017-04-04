class Cursor(object):
    @classmethod
    def mk_list(cls, collection, orig_cursor_list):
        return [cls(collection, orig_cursor)
                for orig_cursor in orig_cursor_list]

    def __init__(self, collection, orig_cursor):
        self.orig_cursor = orig_cursor
        self.collection = collection

    def __getattr__(self, name):
        rtn = getattr(self.orig_cursor, name)
        if isinstance(rtn, dict):
            return self.collection._boxing(rtn)
        return rtn

    def __getitem__(self, index):
        rtn = self.orig_cursor.__getitem__(index)
        if isinstance(rtn, dict):
            return self.collection._boxing(rtn)
        return rtn

    def next(self):
        rtn = self.orig_cursor.next()
        if isinstance(rtn, dict):
            return self.collection._boxing(rtn)
        return rtn

    __next__ = next

    def __copy__(self):
        pass  # TODO
