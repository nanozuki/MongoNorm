"""
MongoNorm
=========

**MongoNorm** is Not a Object Relational Mapping library for mongodb.


MongoNorm just packages document Mongo's as an object. you can add custom
methods and properties for it, And you can still use it as dict.

MongoNorm based on pymongo. The class and methods which is not be mentioned
is same as pymongo's, please refer to pymongo's documentation first.

"""
from setuptools import setup

VERSION = '0.4.0'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    'Topic :: Database',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

with open('README.rst') as f:
    long_desc = f.read()

setup(
    name='MongoNorm',
    version=VERSION,
    url='https://github.com/CrowsT/MongoNorm',
    license='BSD',
    author='Crows',
    author_email='pt.wenhan@gmail.com',
    description="MongoNorm is Not a Object Relational Mapping library "
                "for mongodb.",
    long_description=__doc__,
    packages=['mongonorm'],
    platforms='any',
    install_requires=[
        'PyMongo(>=3.0)'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=CLASSIFIERS
)
