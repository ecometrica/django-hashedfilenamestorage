from __future__ import unicode_literals

from contextlib import contextmanager

import os
import shutil
import warnings

try:
    from warnings import catch_warnings
except ImportError:
    def catch_warnings():
        original_filters = warnings.filters
        try:
            yield
        finally:
            warnings.filters = original_filters

from django.conf import settings
from django.core.files.base import ContentFile
from django.test import TestCase
from django.utils.functional import LazyObject

from django_hashedfilenamestorage.storage import (
    HashedFilenameMetaStorage, HashedFilenameFileSystemStorage,
    NoAvailableName
)


class StubStorage(object):
    def __init__(self):
        pass


class StubSafeStorage(StubStorage):
    def __init__(self, uniquify_names=False, *args, **kwargs):
        # Support uniquify_names as an argument
        super(StubSafeStorage, self).__init__(*args, **kwargs)


def stub_random_string(*args, **kwargs):
    stub_random_string.count += 1
    return str(stub_random_string.count)


class HashedFilenameTestCase(TestCase):
    CONTENT = b'Hello world!'
    SHA1SUM = 'd3486ae9136e7856bc42212385ea797094475802'

    def test_init(self):
        # SafeStorage supports uniquify_names
        HashedFilenameMetaStorage(storage_class=StubSafeStorage)()
        # Normal Storage classes do not
        HashedFilenameMetaStorage(storage_class=StubStorage)()

    def test_get_available_name(self):
        with media_root():
            storage = HashedFilenameFileSystemStorage()
            self.assertRaises(NoAvailableName, storage.get_available_name, '')

    def test_get_content_name(self):
        with media_root():
            storage = HashedFilenameFileSystemStorage()
            self.assertEqual(
                storage._get_content_name(name='',
                                          content=ContentFile(self.CONTENT)),
                '%s' % self.SHA1SUM
            )
            self.assertEqual(
                storage._get_content_name(name='',
                                          content=ContentFile(self.CONTENT),
                                          chunk_size=1),
                '%s' % self.SHA1SUM
            )
            self.assertEqual(
                storage._get_content_name(name='foo',
                                          content=ContentFile(self.CONTENT)),
                '%s' % self.SHA1SUM
            )
            self.assertEqual(
                storage._get_content_name(name='foo.txt',
                                          content=ContentFile(self.CONTENT)),
                '%s.txt' % self.SHA1SUM
            )
            self.assertEqual(
                storage._get_content_name(name='foo/bar',
                                          content=ContentFile(self.CONTENT)),
                'foo/%s' % self.SHA1SUM
            )
            self.assertEqual(
                storage._get_content_name(name='foo/bar.txt',
                                          content=ContentFile(self.CONTENT)),
                'foo/%s.txt' % self.SHA1SUM
            )

    def test_compute_hash(self):
        with media_root():
            storage = HashedFilenameFileSystemStorage()
            self.assertEqual(
                storage._compute_hash(content=ContentFile(self.CONTENT)),
                self.SHA1SUM
            )
            self.assertEqual(
                storage._compute_hash(content=ContentFile(self.CONTENT),
                                      chunk_size=1),
                self.SHA1SUM
            )

    def test_save(self):
        with media_root():
            storage = HashedFilenameFileSystemStorage()
            name1 = storage.save('foo/bar.txt', ContentFile(self.CONTENT))
            self.assertEqual(name1,
                             'foo/%s.txt' % self.SHA1SUM)
            self.assertEqual(storage.open(name1).read(), self.CONTENT)

            storage.delete(name1)
            name2 = storage.save('foo/bar.txt', ContentFile(self.CONTENT))
            self.assertEqual(name2, name1)
            self.assertEqual(storage.open(name2).read(), self.CONTENT)

            name3 = storage.save('foo/another.txt', ContentFile(self.CONTENT))
            self.assertEqual(name3, name1)
            self.assertEqual(storage.open(name3).read(), self.CONTENT)


@contextmanager
def patch(namespace, **values):
    """Patches `namespace`.`name` with `value` for (name, value) in values"""
    originals = {}
    if isinstance(namespace, LazyObject):
        if namespace._wrapped is None:
            namespace._setup()
        namespace = namespace._wrapped
    for (name, value) in values.items():
        try:
            originals[name] = getattr(namespace, name)
        except AttributeError:
            originals[name] = NotImplemented
        if value is NotImplemented:
            if originals[name] is not NotImplemented:
                delattr(namespace, name)
        else:
            setattr(namespace, name, value)
    try:
        yield
    finally:
        for (name, original_value) in originals.items():
            if original_value is NotImplemented:
                if values[name] is not NotImplemented:
                    delattr(namespace, name)
            else:
                setattr(namespace, name, original_value)


@contextmanager
def media_root(dirname='test_media/'):
    if os.path.exists(dirname):
        raise Exception('Cannot run tests safely, %r already exists!' %
                        dirname)
    try:
        with patch(settings, MEDIA_ROOT=dirname):
            yield
    finally:
        shutil.rmtree(dirname, ignore_errors=True)
