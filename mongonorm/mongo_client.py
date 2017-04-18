from pymongo import MongoClient as OrigMongoClient

from mongonorm.database import Database


class OrigClientFactory(object):
    def __init__(self, host=None, port=None, document_class=dict,
                 tz_aware=None, connect=None, **kwargs):
        self.host = host
        self.port = port
        self.document_class = document_class
        self.tz_aware = tz_aware
        self.connect = connect
        self.kwargs = kwargs

    def make(self):
        return OrigMongoClient(self.host, self.port, self.document_class,
                               self.tz_aware, self.connect, **(self.kwargs))


class MongoClient(object):
    def __init__(self, host=None, port=None, document_class=dict,
                 tz_aware=None, connect=None, lazy_load=True, **kwargs):
        if lazy_load is True:
            self._o_client = None
            self._o_client_factory = OrigClientFactory(
                    host=host, port=port, document_class=document_class,
                    tz_aware=tz_aware, connect=connect, **kwargs)
        else:
            self._o_client = MongoClient(
                    host=host, port=port, document_class=document_class,
                    tz_aware=tz_aware, connect=connect, **kwargs)
            self._o_client_factory = None

    @property
    def o_client(self):
        if self._o_client is None:
            self._o_client = self._o_client_factory.make()
        return self._o_client

    def get_o_database(self, name):
        return self.o_client[name]

    def __getattr__(self, name):
        if name in OrigMongoClient.__dict__:
            return self.o_client.__getattr__(name)
        else:
            return Database(self, name)

    def __getitem__(self, item):
        return Database(self, item)
