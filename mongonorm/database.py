from pymongo.database import Database as OrigDatabase

from mongonorm import document


class OrigDatabaseFactory(object):
    def __init__(self, client, name):
        self.client = client
        self.name = name

    def make(self):
        return self.client.o_client[self.name]


class OrigCollectionFactory(object):
    def __init__(self, database, name):
        self.database = database
        self.name = name

    def make(self):
        return self.database.o_database[self.name]


class Database(object):
    def __init__(self, client, name, lazy_load=True):
        if lazy_load is True:
            self._o_database = None
            self._o_database_factory = OrigDatabaseFactory(client, name)
        else:
            self._o_database = OrigDatabase(client, name)
            self._o_database_factory = None

    @property
    def o_database(self):
        if self._o_database is None:
            self._o_database = self._o_database_factory.make()
        return self._o_database

    def __getattr__(self, name):
        raise AttributeError

    def __getitem__(self, item):
        raise KeyError

    def collection(self, name):
        collection_factory = OrigCollectionFactory(self, name)

        def decorator(cls):
            cls._o_collection_factory = collection_factory
            cls._o_collection = None
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
