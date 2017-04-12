MongoNorm
=========

`English documents <README.rst>`_

**MongoNorm** 不是一个Mongodb的ORM库。
MongoNorm仅仅是将Mongo的Document包装为对象，你可以为他添加自定义的方法和属性，
并仍旧可以像使用dict一样使用它。

MongoNorm基于pymongo。没有做出说明的概念和方法，请参考pymongo的文档。

安装
----

使用pip安装::

    pip install MongoNorm

使用
----

1. MongoClient和Database

就像你使用pymongo一样::

    from mongonorm import MongoClient
    client = MongoClient()
    # or: client = MongoClient('mongodb://localhost:27017/')
    db = client.test_database

2. 定义你自己的Model

MongoNorm改变了collection和document的使用方式，首先你需要定义自己所需的Model::

    @db.collection('articles')
    class Article(object):
        """ Article

        documents struct: {
            "title": "article title"
            "author": "author"
            "content": "",
        }
        """
        def __init__(self, title, author, content):
            self.insert({
                'title': title,
                'author': author,
                'content': content})

        def html_content(self):
            parse_html(self['content'])

*!提醒: 关于 __init__()*:

    不要在``__init__()``里面定义属性，如果你需要，可以定义property。

    你必须在 ``__init__()`` 中或者之后调用 ``insert(document)``, 才能将
    document添加到Mongodb

所有pymongo关于collection的操作，都变成了这个Model的classmethod，
如果在pymongo里面返回的是document，则将被monogonorm封装为你定义的类，比如::

    Article.find_one({'title': 'Hello'})  # return an object of Article or None
    cur = Article.find({})
    # return a cursor, you can get Article object from this cusor

    for article in cur:
        print(article['title'])  # use as dict
        print(article.html_content())  # use method of model class

