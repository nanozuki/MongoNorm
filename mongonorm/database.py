from pymongo.database import Database as OrigDatabase

from mongonorm import document


class Database(OrigDatabase):
    def __getattr__(self, name):
        raise AttributeError

    def __getitem__(self, item):
        raise KeyError

    def collection(self, name):
        collection = super(Database, self).__getitem__(name)

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
