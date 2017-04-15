from .model import TheModel


def test_create_n_read_single_doc():
    TheModel.delete_many({})
    assert TheModel.find_one() is None
    tm = TheModel(2)
    assert isinstance(tm, TheModel) is True
    assert tm['test_id'] == 2


def test_create_n_read_multi_doc():
    TheModel.delete_many({})
    for i in range(10):
        TheModel(i)
    assert TheModel.find().count() == 10
    cur = TheModel.find().sort('test_id')
    assert cur[5].get_id() == 5
    cur = TheModel.find().sort('test_id')
    ids = [tm.get_id() for tm in cur[2:7]]
    assert ids == list(range(2, 7))


def test_update():
    def ensure_test_id(test_id):
        assert tm.get_id() == test_id
        orig_doc = TheModel.__collection__.find_one({'_id': oid})
        assert orig_doc['test_id'] == test_id

    TheModel.delete_many({})
    tm = TheModel(2)
    oid = tm.oid
    tm['test_id'] = 3
    ensure_test_id(3)
    tm.update({'$set': {'test_id': 4}})
    ensure_test_id(4)
    TheModel.update_one({'test_id': 4}, {'$set': {'test_id': 5}})
    tm.reload()
    ensure_test_id(5)
    tm.replace({'test_id': 6})
    ensure_test_id(6)
