from bson import ObjectId
from bson.errors import InvalidId


class Collection(object):
    """ Proxy of pymongo's Collection

    :Attributes
        :collection :pymongo.collection  reference for collection of pymongo
        :primary_fields: [str] fields like primary key
        :default_values: {} default_values

    :Usage
        class MyModel(DocProxy):
            collection = db.my_model
            default_values = {"name": "", "create_time": datetime.now()}

            def __init__(self, **kwargs):
                doc = make_doc() ## make an document by kwargs
                self.insert(doc)
    """
    collection = None
    default_values = {}

    def _find_doc(self, filter_obj):
        return self.collection.find_one(filter_obj)

    def _check_bound(self):
        if self._doc is None and self._id is None:
            raise ValueError("DocProxy '{}' bind Nothing".format(
                self.__class__.__name__))
        elif self._doc is None:
            self._doc = self._find_doc({'_id': self._id})
        elif self._id is None:
            self._id = self._doc['_id']

    @classmethod
    def boxing(cls, doc):
        obj = cls.__new__(cls)
        obj._doc = doc
        obj._id = doc['_id']
        return obj

    @property
    def oid(self):
        self._check_bound()
        return self._id

    @property
    def raw(self):
        self._check_bound()
        return self._doc

    def __getitem__(self, item):
        if item in self.raw:
            return self.raw[item]
        elif item in self.default_values:
            return self.default_values[item]
        else:
            raise KeyError(item)

    def __setitem__(self, key, value):
        self.collection.update_one({'_id': self.oid}, {'$set': {key: value}})
        self._doc = None

    def insert(self, doc):
        result = self.collection.insert_one(doc)
        self._id = result.inserted_id
        self._doc = self.collection.find_one({'_id': self._id})

    def update(self, update_obj):
        self.collection.update_one({'_id': self._id}, update_obj)
        self._doc = None

    def reload(self):
        self._check_bound()
        self._doc = None

    def __repr__(self):
        return "<Collection.{0} id {1}>".format(
            self.__class__.__name__, self._id)
