from .model import TheModel


def test_boxing():
    tm = TheModel.find_one({})
    assert isinstance(tm, TheModel)
    assert tm['test_id'] is not None
