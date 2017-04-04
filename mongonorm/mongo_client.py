from pymongo import MongoClient as OrigMongoClient
from pymongo.database import Database as OrigDataBase

from mongonorm.database import DataBase


class MongoClient(object):
    def __init__(self, host=None, port=None, tz_aware=None,
                 connect=None, **kwargs):
        self.mongo_client = OrigMongoClient(host, port, dict, tz_aware,
                                            connect, **kwargs)

    def __repr__(self):
        return self.mongo_client.__repr__()

    def __getattr__(self, name):
        rtn = self.mongo_client.__getattr__(name)
        if isinstance(rtn, OrigDataBase) is True:
            return DataBase(rtn)
        return rtn

    def __getitem__(self, name):
        rtn = self.mongo_client.__getitem__(name)
        if isinstance(rtn, OrigDataBase) is True:
            return DataBase(rtn)
        return rtn
