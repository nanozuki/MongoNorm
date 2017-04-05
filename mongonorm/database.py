from mongonorm import document


class DataBase(object):
    def __init__(self, orig_database):
        self.orig_database = orig_database

    def __getattr__(self, name):
        return getattr(self.orig_database, name)

    def register(self, collection):
        collection = self.orig_database[collection]

        def decorator(cls):
            cls.__collection__ = collection
            if 'default_values' not in cls.__dict__:
                setattr(cls, 'default_values', {})
            for method in document.property_methods:
                setattr(cls, method, property(getattr(document, method)))
            for method in document.class_methods:
                setattr(cls, method, classmethod(getattr(document, method)))
            for method in document.normal_methods:
                setattr(cls, method, getattr(document, method))
            return cls
        return decorator
