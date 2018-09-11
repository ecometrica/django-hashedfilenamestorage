.. image:: https://travis-ci.org/ecometrica/django-hashedfilenamestorage.svg?branch=master
    :target: https://travis-ci.org/ecometrica/django-hashedfilenamestorage

``django-hashedfilenamestorage``
================================

A Django storage backend that names files by hash value.

By default, ``django.core.files.storage.FileSystemStorage`` deals with
conflicting filenames by appending an underscore and a random 7
character alphanumeric string to the file. For
instance, if you try to create ``hello.txt`` when it already exists,
it will rename it as e.g. ``hello_a12mkj3.txt``.

``django-hashedfilenamestorage`` creates hashed filenames, so if you
try to create ``hello.txt`` with the content ``Hello world!``, it will
save it as ``d3486ae9136e7856bc42212385ea797094475802.txt``. Directory
names and extensions are preserved, only the root filename is
changed. This reduces the number of duplicates stored in the
underlying backend, and implies that these files can be served from a
static cache that never expires.

Installing
----------

The easiest way to install ``django-hashedfilenamestorage`` is to use
**pip**::

    pip install django-hashedfilenamestorage


Quick Start
-----------

In your Django ``settings`` file:

* Set ``DEFAULT_FILE_STORAGE`` to
  ``'django_hashedfilenamestorage.storage.HashedFilenameFileSystemStorage'``

This gives you hashed filenames, backed on Django's
``FileSystemStorage`` storage class.


``HashedFilenameMetaStorage``
-----------------------------

You can define a new underlying storage class by using
``HashedFilenameMetaStorage`` to wrap it::

    from django.core.files.storage import get_storage_class

    from django_hashedfilenamestorage.storage import HashedFilenameMetaStorage

    HashedFilenameMyStorage = HashedFilenameMetaStorage(
        storage_class=get_storage_class('myapp.storage.MyStorage'),
    )


Hashing algorithm
-----------------

HashedFilenameMetaStorage is meant to generate duplicate filenames for
files with identical contents. To do this, it reads the contents of
the file and generates a SHA-1 hash of them.

Filenames have their extensions preserved, so it is possible to have
duplicate contents on the filesystem, but it is important to help
serve files with their proper content types.
