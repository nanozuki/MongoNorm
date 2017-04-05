from mongonorm.mongo_client import MongoClient


mc = MongoClient()
db = mc.test


@db.register(collection='test')
class TheModel(object):
    def __init__(self, n):
        self.insert({"test_id": n})
