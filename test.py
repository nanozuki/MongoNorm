from mongonorm.mongo_client import MongoClient


mc = MongoClient()
db = mc.test


@db.register(name='test')
class TestModel(object):
    def __init__(self, n):
        self.insert({"test_id": n})


ntm = TestModel(1)
tm = TestModel.find_one({'test_id': 1})
print(tm.raw)

