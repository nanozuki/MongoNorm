from setuptools import setup

VERSION = '0.1.1'

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
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
    'Topic :: Software Development :: Libraries :: Python Modules',
]

with open('README.md') as f:
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
    long_description=long_desc,
    packages=['mongonorm'],
    platforms='any',
    install_requires=[
        'PyMongo(>=3.0)'
    ],
    classifiers=CLASSIFIERS
)
