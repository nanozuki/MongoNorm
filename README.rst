MongoNorm
=========

`中文文档 <README_cn.rst>`_

**MongoNorm** is Not a Object Relational Mapping library for mongodb.


MongoNorm just packages document Mongo's as an object, you can add custom methods 
and properties for him, And you can still use it as dict.

MongoNorm based on pymongo. The class and methos which is not be mentioned
is same as pymongo's, please refer to pymongo's documentation first.

installation
------------
Use pip to install::
    pip install MongoNorm

use guide
---------

1. MongoClient and Database

Use these just like you use in pymongo::

    from mongonorm import MongoClient
    client = MongoClient()
    # Or: client = MongoClient('mongodb://localhost:27017/')
    db = client.test_database

2. Define your own Model

MongoNorm changed the way collections and documents were used,
first you need to define your own Model::

    @db.collection('articles')
    Class Article (object):
        """Article

        documents struct: {
            "title": "article title",
            "author": "author",
            "content": "",
        }
        """
        def __init__(self, title, author, content):
            Self.insert ({
                'Title': title,
                'Author': author,
                'Content': content})

        def html_content(self):
            parse_html(self['content'])

All the pymongo on the collection of operations,
have become the Model of the classmethod,
If the pymongo inside is the document, will be monogonorm package
for your definition of the class, such as::
    
    Article.find_one ({'title': 'Hello'}) # return an object of Article or None
    Cur = Article.find ({})
    # Return a cursor, you can get Article object from this cusor
    
    For article in cur:
        Print (article ['title']) # use as dict
        Print (article.html_content ()) # use method of model class

