from pymongo import MongoClient as OrigMongoClient
from pymongo.database import Database as OrigDatabase

from mongonorm.database import Database


class MongoClient(OrigMongoClient):
    def __getattr__(self, name):
        attr = super(MongoClient, self).__getattr__(name)
        if isinstance(attr, OrigDatabase):
            return Database(self, name)
        return attr

    def __getitem__(self, item):
        attr = super(MongoClient, self).__getitem__(item)
        if isinstance(attr, OrigDatabase):
            return Database(self, item)
        return attr
