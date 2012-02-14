Introduction
=============

*restsims* is a small pyramid restfull wrapper around simserver itself.

It provides a basic HTML interface to test and play around with the service.

_WARNING!_

restsims does not yet do authentication so you
do NOT want to USE it on a PUBLIC network

INSTALL
========

You may want to install the server in a clean and repeatable way using
virtual environment and buildout.

::

    $ mkdir simserver
    $ virtualenv --python=bin/python2.7 simserver/
    $ mkdir buildout-cache
    $ mkdir buildout-cache/eggs
    $ mkdir buildout-cache/downloads
    $ mkdir src # for  LAPACK, BLAS and restsims
    $ wget http://python-distribute.org/bootstrap.py

restsims comes with an example buildout.cfg file
in the tarball, or you find it on github.

copy buildout.cfg into the simserver directory

::

    $ bin/python bootstrap.py

you can try to easy_install numpy and scipy

::

    $ bin/easy_install numpy
    $ bin/easy_install scipy

but this never worked for me so i installed it from source
http://www.scipy.org/Download
as documented in
http://scipy.org/Installing_SciPy/BuildingGeneral
the buildout assumes that LAPACK and BLAS are installed in the src
directory


test if numpy and scipy are installed correctly:

::

    $ bin/python
    >>> import numpy
    >>> import scipy
    >>>

run buildout

::

$ bin/buildout

The buildout will take a while and install all the dependencies
for the server. Start the server with:

::

    $ bin/pserve src/restsims/development.ini

Now you can access the server at http://localhost:6543/


Configuration
==============

The configuration is done in two ini files one for developement
and another one for production

Things you might want to change:

at the beginning of the file:

::

    port = 6543

is the port restsims listens on.

At the end of the file

::

    [simserver]
    path=/tmp/simmserver/

is the location of the simserver index


API
====

Restsims is meant to be used as a service to be called from other
applications. It returns its results as html or JSON. The HTML view is
meant for experiments and to make yourself aquainted with the
calls and responses.



status
-------

To find out if your restsims server and simservice is running:

::

    Request = {'format': 'json', 'action': 'status'}

    Response = {'status': 'OK', 'response': service.status}

service.status gives you some information about you index.


train
------

To be able to extract information from the API you first need to
build a corpus. The service indexes documents in a semantic
representation so we must teach the service how to convert between plain
text and semantics first.

For the semantic model to make sense, it has to be trained on a corpus that is:

- Reasonably similar to (or the same as/ a subset of) the documents you
  want to index later.
  Training on a corpus of recipes in French when all indexed documents
  will be about programming in English will not help.

- Reasonably large (at least thousands of documents), so that the
  statistical analysis has a chance to kick in.


Note that each time your train the corpus
the index is destroyed and you must reindex all documents.

Pass 'text' as the plain texts and the uids of the documents as a
list of dictionaries {'id': UID, 'text': Text}

::

    Request = {'format': 'json', 'action': 'train',
            'text': [{'id': UID, 'text': Text}]}


If you prefer to tokenize the texts yourself, you can pass 'text' as
a list of dictionaries {'id': UID, 'tokens': ['List', 'of', 'tokens']}

::

    Request = {'format': 'json', 'action': 'train',
            'text': [{'id': UID, 'tokens': ['List', 'of', 'tokens']}]

You may also upload a compressed file (tar.gz or tar.bz2) in which each
contained file is the plain text representation of your document to train
your index and the filename equals the UID of the document.

::

    Request = {'format': 'json', 'action': 'train',
            'data': file}


All three request variants will return:

::

    Response = {'status': 'OK', 'response': i}

where i is the number of documents on which the index was trained
or an http error if not successfull.


index
------

When you pass documents that have the same uid as some already indexed
document, the indexed document is overwritten by the new input.
You don’t have to index all documents first to start querying,
indexing can be incremental.

The request formats are the same as for training the corpus:

::

    Request = {'format': 'json', 'action': 'index',
                'text': [{'id': UID, 'text': Text}]}

    Request = {'format': 'json', 'action': 'index',
                'text': [{'id': UID, 'tokens': ['List', 'of', 'tokens']}]

    Request = {'format': 'json', 'action': 'index',
                'data': file}


    Response = {'status': 'OK', 'response': i}

where i is the number of documents indexed.


query
------

There are two types of queries:

By a plain text that will be compared to the indexed documents

::

    Request = {'format': 'json', 'action': 'query',
            'text': 'some free text you want to find similar items to'}

    Response = {'status': 'OK', 'response':

e.g.

::

    {'status': 'OK', 'response': [('e82c58f43cec4db96f0cda25e5a1b2ba', 0.6676519513130188, None),
    ('13ea18dd855582ad23c9dabf5041aa1a', 0.6201680898666382, None),
    ('89734760899b4324fe9dff147d842b2b', 0.5058814883232117, None)]}


By a list of documents [UID,]

::

    Request = {'format': 'json', 'action': 'query',
            'text': [UID,]}

    Response = {'status': 'OK', 'response': {
    'uid1': [similar docs], 'uid2': [similar docs], ...}


e.g.

::

    {'status': 'OK', 'response':
        {u'7d6342a60159eca02b54340c3d352ecd':
            [('7d6342a60159eca02b54340c3d352ecd', 1.0, None),
            ('89734760899b4324fe9dff147d842b2b', 0.86540287733078, None),
            ('cab7138af0bde9f8d05dfadc731ffcf1', 0.8373217582702637, None)],
        u'e82c58f43cec4db96f0cda25e5a1b2ba':
            [('e82c58f43cec4db96f0cda25e5a1b2ba', 1.0, None),
            ('13ea18dd855582ad23c9dabf5041aa1a', 0.871651291847229, None),
            ('15143b79edfa02c60f7248cb4b29537c', 0.865399181842804, None))]}}




optimize
---------

To optimize the index for size and speed after indexing:

::

    Request = {'format': 'json', 'action': 'optimize'}

    Response = {'status': 'OK', 'response': 'index optimized'}


delete
--------

Delete documents with a list of document uids to be removed from the index:

::

    Request = {'format': 'json', 'action': 'delete',
            'text': [UID]}

    Response = {'status': 'OK', 'response': 'documents deleted'}



documents
----------

This return the UIDs of all you indexed documents:

::

    Request = {'format': 'json', 'action': 'documents'}

    Response = {'status': 'OK', 'response': service.keys}


is_indexed
-----------

To find out if a certain document is in the index:

::

    Request = {'format': 'json', 'action': 'query',
            'text': UID}

    Response = {'status': 'OK', 'response': True/False}


Links
=====

- Code repository: https://github.com/cleder/restsims
- Questions and comments to gensim@googlegroups.com
- Report bugs at https://github.com/cleder/restsims/issues
