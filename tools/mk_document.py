#!/usr/bin/env python3
import re

properties = [
    "def full_name(self):",
    "def name(self):",
    "def database(self):"]

normal_fun = [
    "def with_options(self, codec_options=None, read_preference=None, write_concern=None, read_concern=None):",
    "def initialize_unordered_bulk_op(self, bypass_document_validation=False):",
    "def initialize_ordered_bulk_op(self, bypass_document_validation=False):",
    "def bulk_write(self, requests, ordered=True, bypass_document_validation=False):",
    "def insert_one(self, document, bypass_document_validation=False):",
    "def insert_many(self, documents, ordered=True, bypass_document_validation=False):",
    "def replace_one(self, filter, replacement, upsert=False, bypass_document_validation=False, collation=None):",
    "def update_one(self, filter, update, upsert=False, bypass_document_validation=False, collation=None):",
    "def update_many(self, filter, update, upsert=False, bypass_document_validation=False, collation=None):",
    "def drop(self):",
    "def delete_one(self, filter, collation=None):",
    "def delete_many(self, filter, collation=None):",
    "def count(self, filter=None, **kwargs):",
    "def create_indexes(self, indexes):",
    "def create_index(self, keys, **kwargs):",
    "def drop_indexes(self):",
    "def drop_index(self, index_or_name):",
    "def reindex(self):",
    "def list_indexes(self):",
    "def index_information(self):",
    "def options(self):",
    "def aggregate(self, pipeline, **kwargs):",
    "def group(self, key, condition, initial, reduce, finalize=None, **kwargs):",
    "def rename(self, new_name, **kwargs):",
    "def distinct(self, key, filter=None, **kwargs):",
    "def map_reduce(self, map, reduce, out, full_response=False, **kwargs):",
    "def inline_map_reduce(self, map, reduce, full_response=False, **kwargs):",
]

cursor_fun = [
    "def find(self, *args, **kwargs):",
]

cursors_fun = [
    "def parallel_scan(self, num_cursors, **kwargs):",
]

doc_fun = [
    "def find_one(self, filter=None, *args, **kwargs):",
    "def find_one_and_delete(self, filter, projection=None, sort=None, **kwargs):",
    "def find_one_and_replace(self, filter, replacement, projection=None, sort=None, upsert=False, return_document=ReturnDocument.BEFORE, **kwargs):",
    "def find_one_and_update(self, filter, update, projection=None, sort=None, upsert=False, return_document=ReturnDocument.BEFORE, **kwargs):",
]


collection_py = """from mongonorm.cursor import Cursor
from pymongo import ReturnDocument


property_methods = [
{0}
    'oid',
    'raw',
]

class_methods = [
{1}
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


{2}


def _find_doc(self, filter_obj):
    return self.o_collection().find_one(filter_obj)


def _check_bound(self):
    if self._doc is None and self._id is None:
        raise ValueError("DocProxy '{{}}' bind Nothing".format(
            self.__class__.__name__))
    elif self._doc is None:
        self._doc = self._find_doc({{'_id': self._id}})
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
    self.o_collection().update_one({{'_id': self.oid}}, {{'$set': {{key: value}}}})
    self._doc = None


def copy(self):
    rtn = self.raw
    self._doc = None
    return rtn


def insert(self, doc):
    result = self.o_collection().insert_one(doc)
    self._id = result.inserted_id
    self._doc = self.o_collection().find_one({{'_id': self._id}})


def update(self, update_obj):
    self.o_collection().update_one({{'_id': self._id}}, update_obj)
    self._doc = None


def replace(self, replace_obj):
    self.o_collection().replace_one({{'_id': self._id}}, replace_obj)
    self._doc = None


def reload(self):
    self._check_bound()
    self._doc = None


def __repr__(self):
    return "<Document.{{0}} id {{1}}>".format(
        self.__class__.__name__, self._id)
"""


def make_document_py():
    fun_defs = []
    property_methods = []
    class_methods = []
    for fun in properties:
        name, define = make_fun(fun, property_=True)
        property_methods.append("    '{0}',".format(name))
        fun_defs.append(define)
    for fun in normal_fun:
        name, define = make_fun(fun)
        class_methods.append("    '{0}',".format(name))
        fun_defs.append(define)
    for fun in cursor_fun:
        name, define = make_fun(fun, 'cursor')
        class_methods.append("    '{0}',".format(name))
        fun_defs.append(define)
    for fun in cursors_fun:
        name, define = make_fun(fun, 'cursors')
        class_methods.append("    '{0}',".format(name))
        fun_defs.append(define)
    for fun in doc_fun:
        name, define = make_fun(fun, 'doc')
        class_methods.append("    '{0}',".format(name))
        fun_defs.append(define)

    collection_py_content = collection_py.format(
        '\n'.join(property_methods),
        '\n'.join(class_methods),
        '\n\n\n'.join(fun_defs))
    with open('mongonorm/document.py', 'w') as f:
        f.write(collection_py_content)


def make_fun(line, return_type='', property_=False):
    def_re = re.compile(r'^def (.*)\((.*)\):')
    define = def_re.match(line)
    fun_name = define.group(1)
    params = define.group(2).split(', ')
    if property_ is False:
        params[0] = 'cls'
    def_params = ', '.join(params)
    call_params = ', '.join([single_param(p) for p in params[1:]])

    if return_type == '':
        call = 'cls' if property_ is False else 'self'
        return fun_name, "def {0}({1}):\n    return {3}.o_collection().{0}({2})".format(fun_name, def_params, call_params, call)
    elif return_type == 'cursor':
        return fun_name, "def {0}({1}):\n    return Cursor(cls, cls.o_collection().{0}({2}))".format(fun_name, def_params, call_params)
    elif return_type == 'cursors':
        return fun_name, "def {0}({1}):\n    return Cursor.mk_list(cls, cls.o_collection().{0}({2}))".format(fun_name, def_params, call_params)
    elif return_type == 'doc':
        return fun_name, "def {0}({1}):\n    return cls._boxing(cls.o_collection().{0}({2}))".format(fun_name, def_params, call_params)


def single_param(p):
    m = re.match(r'(.*)=(.*)', p)
    if m is not None:
        return m.group(1)
    else:
        return p


if __name__ == '__main__':
    make_document_py()
