from mongonorm import collection


class DataBase(object):
    def __init__(self, orig_database):
        self.orig_database = orig_database

    def __getattr__(self, name):
        return getattr(self.orig_database, name)

    def register(self, name):
        collec = self.orig_database[name]

        def decorator(cls):
            cls.__collection__ = collec
            for method in collection.property_methods:
                cls.__dict__[method] = property(getattr(collection, method))
            for method in collection.class_methods:
                cls.__dict__[method] = classmethod(getattr(collection, method))
            for method in collection.normal_methods:
                cls.__dict__[method] = getattr(collection, method)
            return cls
        return decorator
