class Cursor(object):
    @classmethod
    def mk_list(cls, orig_cursor_list):
        return [cls(orig_cursor) for orig_cursor in orig_cursor_list]

    def __init__(self, orig_cursor):
        self.orig_cursor = orig_cursor
