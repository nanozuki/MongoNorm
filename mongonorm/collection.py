from mongonorm.cursor import Cursor
from pymongo import ReturnDocument


property_methods = [
    'full_name',
    'name',
    'database',
    'oid',
    'raw',
]

class_methods = [
    'with_options',
    'initialize_unordered_bulk_op',
    'initialize_ordered_bulk_op',
    'bulk_write',
    'insert_one',
    'insert_many',
    'replace_one',
    'update_one',
    'update_many',
    'drop',
    'delete_one',
    'delete_many',
    'count',
    'create_indexes',
    'create_index',
    'drop_indexes',
    'drop_index',
    'reindex',
    'list_indexes',
    'index_information',
    'options',
    'aggregate',
    'group',
    'rename',
    'distinct',
    'map_reduce',
    'inline_map_reduce',
    'find',
    'parallel_scan',
    'find_one',
    'find_one_and_delete',
    'find_one_and_replace',
    'find_one_and_update',
    '_boxing'
]

normal_methods = [
    '_find_doc',
    '_check_bound',
    '__repr__',
    '__getitem__',
    '__setitem__',
    'insert',
    'update',
    'reload',
]


def full_name(self):
    return self.__collection__.full_name()


def name(self):
    return self.__collection__.name()


def database(self):
    return self.__collection__.database()


def with_options(cls, codec_options=None, read_preference=None, write_concern=None, read_concern=None):
    return cls.__collection__.with_options(codec_options, read_preference, write_concern, read_concern)


def initialize_unordered_bulk_op(cls, bypass_document_validation=False):
    return cls.__collection__.initialize_unordered_bulk_op(bypass_document_validation)


def initialize_ordered_bulk_op(cls, bypass_document_validation=False):
    return cls.__collection__.initialize_ordered_bulk_op(bypass_document_validation)


def bulk_write(cls, requests, ordered=True, bypass_document_validation=False):
    return cls.__collection__.bulk_write(requests, ordered, bypass_document_validation)


def insert_one(cls, document, bypass_document_validation=False):
    return cls.__collection__.insert_one(document, bypass_document_validation)


def insert_many(cls, documents, ordered=True, bypass_document_validation=False):
    return cls.__collection__.insert_many(documents, ordered, bypass_document_validation)


def replace_one(cls, filter, replacement, upsert=False, bypass_document_validation=False, collation=None):
    return cls.__collection__.replace_one(filter, replacement, upsert, bypass_document_validation, collation)


def update_one(cls, filter, update, upsert=False, bypass_document_validation=False, collation=None):
    return cls.__collection__.update_one(filter, update, upsert, bypass_document_validation, collation)


def update_many(cls, filter, update, upsert=False, bypass_document_validation=False, collation=None):
    return cls.__collection__.update_many(filter, update, upsert, bypass_document_validation, collation)


def drop(cls):
    return cls.__collection__.drop()


def delete_one(cls, filter, collation=None):
    return cls.__collection__.delete_one(filter, collation)


def delete_many(cls, filter, collation=None):
    return cls.__collection__.delete_many(filter, collation)


def count(cls, filter=None, **kwargs):
    return cls.__collection__.count(filter, **kwargs)


def create_indexes(cls, indexes):
    return cls.__collection__.create_indexes(indexes)


def create_index(cls, keys, **kwargs):
    return cls.__collection__.create_index(keys, **kwargs)


def drop_indexes(cls):
    return cls.__collection__.drop_indexes()


def drop_index(cls, index_or_name):
    return cls.__collection__.drop_index(index_or_name)


def reindex(cls):
    return cls.__collection__.reindex()


def list_indexes(cls):
    return cls.__collection__.list_indexes()


def index_information(cls):
    return cls.__collection__.index_information()


def options(cls):
    return cls.__collection__.options()


def aggregate(cls, pipeline, **kwargs):
    return cls.__collection__.aggregate(pipeline, **kwargs)


def group(cls, key, condition, initial, reduce, finalize=None, **kwargs):
    return cls.__collection__.group(key, condition, initial, reduce, finalize, **kwargs)


def rename(cls, new_name, **kwargs):
    return cls.__collection__.rename(new_name, **kwargs)


def distinct(cls, key, filter=None, **kwargs):
    return cls.__collection__.distinct(key, filter, **kwargs)


def map_reduce(cls, map, reduce, out, full_response=False, **kwargs):
    return cls.__collection__.map_reduce(map, reduce, out, full_response, **kwargs)


def inline_map_reduce(cls, map, reduce, full_response=False, **kwargs):
    return cls.__collection__.inline_map_reduce(map, reduce, full_response, **kwargs)


def find(cls, *args, **kwargs):
    return Cursor(cls, cls.__collection__.find(*args, **kwargs))


def parallel_scan(cls, num_cursors, **kwargs):
    return Cursor.mk_list(cls, cls.__collection__.parallel_scan(num_cursors, **kwargs))


def find_one(cls, filter=None, *args, **kwargs):
    return cls._boxing(cls.__collection__.find_one(filter, *args, **kwargs))


def find_one_and_delete(cls, filter, projection=None, sort=None, **kwargs):
    return cls._boxing(cls.__collection__.find_one_and_delete(filter, projection, sort, **kwargs))


def find_one_and_replace(cls, filter, replacement, projection=None, sort=None, upsert=False, return_document=ReturnDocument.BEFORE, **kwargs):
    return cls._boxing(cls.__collection__.find_one_and_replace(filter, replacement, projection, sort, upsert, return_document, **kwargs))


def find_one_and_update(cls, filter, update, projection=None, sort=None, upsert=False, return_document=ReturnDocument.BEFORE, **kwargs):
    return cls._boxing(cls.__collection__.find_one_and_update(filter, update, projection, sort, upsert, return_document, **kwargs))


def _find_doc(self, filter_obj):
    return self.__collection__.find_one(filter_obj)


def _check_bound(self):
    if self._doc is None and self._id is None:
        raise ValueError("DocProxy '{}' bind Nothing".format(
            self.__class__.__name__))
    elif self._doc is None:
        self._doc = self._find_doc({'_id': self._id})
    elif self._id is None:
        self._id = self._doc['_id']


def _boxing(cls, doc):
    obj = cls.__new__(cls)
    obj._doc = doc
    obj._id = doc['_id']
    return obj


def oid(self):
    self._check_bound()
    return self._id


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
    self.__collection__.update_one({'_id': self.oid}, {'$set': {key: value}})
    self._doc = None


def insert(self, doc):
    result = self.__collection__.insert_one(doc)
    self._id = result.inserted_id
    self._doc = self.__collection__.find_one({'_id': self._id})


def update(self, update_obj):
    self.__collection__.update_one({'_id': self._id}, update_obj)
    self._doc = None


def reload(self):
    self._check_bound()
    self._doc = None


def __repr__(self):
    return "<Collection.{0} id {1}>".format(
        self.__class__.__name__, self._id)
