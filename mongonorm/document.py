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
    'o_collection',
    '_boxing'
]

normal_methods = [
    '_find_doc',
    '_check_bound',
    '__repr__',
    '__getitem__',
    '__setitem__',
    'copy',
    'insert',
    'update',
    'replace',
    'reload'
]


def full_name(self):
    return self.o_collection().full_name()


def name(self):
    return self.o_collection().name()


def database(self):
    return self.o_collection().database()


def with_options(cls, codec_options=None, read_preference=None, write_concern=None, read_concern=None):
    return cls.o_collection().with_options(codec_options, read_preference, write_concern, read_concern)


def initialize_unordered_bulk_op(cls, bypass_document_validation=False):
    return cls.o_collection().initialize_unordered_bulk_op(bypass_document_validation)


def initialize_ordered_bulk_op(cls, bypass_document_validation=False):
    return cls.o_collection().initialize_ordered_bulk_op(bypass_document_validation)


def bulk_write(cls, requests, ordered=True, bypass_document_validation=False):
    return cls.o_collection().bulk_write(requests, ordered, bypass_document_validation)


def insert_one(cls, document, bypass_document_validation=False):
    return cls.o_collection().insert_one(document, bypass_document_validation)


def insert_many(cls, documents, ordered=True, bypass_document_validation=False):
    return cls.o_collection().insert_many(documents, ordered, bypass_document_validation)


def replace_one(cls, filter, replacement, upsert=False, bypass_document_validation=False, collation=None):
    return cls.o_collection().replace_one(filter, replacement, upsert, bypass_document_validation, collation)


def update_one(cls, filter, update, upsert=False, bypass_document_validation=False, collation=None):
    return cls.o_collection().update_one(filter, update, upsert, bypass_document_validation, collation)


def update_many(cls, filter, update, upsert=False, bypass_document_validation=False, collation=None):
    return cls.o_collection().update_many(filter, update, upsert, bypass_document_validation, collation)


def drop(cls):
    return cls.o_collection().drop()


def delete_one(cls, filter, collation=None):
    return cls.o_collection().delete_one(filter, collation)


def delete_many(cls, filter, collation=None):
    return cls.o_collection().delete_many(filter, collation)


def count(cls, filter=None, **kwargs):
    return cls.o_collection().count(filter, **kwargs)


def create_indexes(cls, indexes):
    return cls.o_collection().create_indexes(indexes)


def create_index(cls, keys, **kwargs):
    return cls.o_collection().create_index(keys, **kwargs)


def drop_indexes(cls):
    return cls.o_collection().drop_indexes()


def drop_index(cls, index_or_name):
    return cls.o_collection().drop_index(index_or_name)


def reindex(cls):
    return cls.o_collection().reindex()


def list_indexes(cls):
    return cls.o_collection().list_indexes()


def index_information(cls):
    return cls.o_collection().index_information()


def options(cls):
    return cls.o_collection().options()


def aggregate(cls, pipeline, **kwargs):
    return cls.o_collection().aggregate(pipeline, **kwargs)


def group(cls, key, condition, initial, reduce, finalize=None, **kwargs):
    return cls.o_collection().group(key, condition, initial, reduce, finalize, **kwargs)


def rename(cls, new_name, **kwargs):
    return cls.o_collection().rename(new_name, **kwargs)


def distinct(cls, key, filter=None, **kwargs):
    return cls.o_collection().distinct(key, filter, **kwargs)


def map_reduce(cls, map, reduce, out, full_response=False, **kwargs):
    return cls.o_collection().map_reduce(map, reduce, out, full_response, **kwargs)


def inline_map_reduce(cls, map, reduce, full_response=False, **kwargs):
    return cls.o_collection().inline_map_reduce(map, reduce, full_response, **kwargs)


def find(cls, *args, **kwargs):
    return Cursor(cls, cls.o_collection().find(*args, **kwargs))


def parallel_scan(cls, num_cursors, **kwargs):
    return Cursor.mk_list(cls, cls.o_collection().parallel_scan(num_cursors, **kwargs))


def find_one(cls, filter=None, *args, **kwargs):
    return cls._boxing(cls.o_collection().find_one(filter, *args, **kwargs))


def find_one_and_delete(cls, filter, projection=None, sort=None, **kwargs):
    return cls._boxing(cls.o_collection().find_one_and_delete(filter, projection, sort, **kwargs))


def find_one_and_replace(cls, filter, replacement, projection=None, sort=None, upsert=False, return_document=ReturnDocument.BEFORE, **kwargs):
    return cls._boxing(cls.o_collection().find_one_and_replace(filter, replacement, projection, sort, upsert, return_document, **kwargs))


def find_one_and_update(cls, filter, update, projection=None, sort=None, upsert=False, return_document=ReturnDocument.BEFORE, **kwargs):
    return cls._boxing(cls.o_collection().find_one_and_update(filter, update, projection, sort, upsert, return_document, **kwargs))


def _find_doc(self, filter_obj):
    return self.o_collection().find_one(filter_obj)


def _check_bound(self):
    if self._doc is None and self._id is None:
        raise ValueError("DocProxy '{}' bind Nothing".format(
            self.__class__.__name__))
    elif self._doc is None:
        self._doc = self._find_doc({'_id': self._id})
    elif self._id is None:
        self._id = self._doc['_id']


def _boxing(cls, doc):
    if doc is None:
        return None

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


def o_collection(cls):
    if cls._o_collection is None:
        cls._o_collection = cls._o_collection_factory.make()
    return cls._o_collection


def __getitem__(self, item):
    if item in self.raw:
        return self.raw[item]
    elif item in self.default_values:
        return self.default_values[item]
    else:
        raise KeyError(item)


def __setitem__(self, key, value):
    self.o_collection().update_one({'_id': self.oid}, {'$set': {key: value}})
    self._doc = None


def copy(self):
    rtn = self.raw
    self._doc = None
    return rtn


def insert(self, doc):
    result = self.o_collection().insert_one(doc)
    self._id = result.inserted_id
    self._doc = self.o_collection().find_one({'_id': self._id})


def update(self, update_obj):
    self.o_collection().update_one({'_id': self._id}, update_obj)
    self._doc = None


def replace(self, replace_obj):
    self.o_collection().replace_one({'_id': self._id}, replace_obj)
    self._doc = None


def reload(self):
    self._check_bound()
    self._doc = None


def __repr__(self):
    return "<Document.{0} id {1}>".format(
        self.__class__.__name__, self._id)
