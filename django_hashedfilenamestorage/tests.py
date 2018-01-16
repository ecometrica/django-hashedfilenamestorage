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
    CONTENT = 'Hello world!'
    BCONTENT = b'Hello world!'
    SHA1SUM = 'd3486ae9136e7856bc42212385ea797094475802'

    def test_init(self):
        # SafeStorage supports uniquify_names
        HashedFilenameMetaStorage(storage_class=StubSafeStorage)()
        # Normal Storage classes do not
        HashedFilenameMetaStorage(storage_class=StubStorage)()

    def test_get_available_name(self):
        with media_root():
            storage = HashedFilenameFileSystemStorage()
            self.assertEqual(storage.get_available_name('foo.txt'), 'foo.txt')

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

    def test_get_bytes_content_name(self):
        with media_root():
            storage = HashedFilenameFileSystemStorage()
            self.assertEqual(
                storage._get_content_name(name='',
                                          content=ContentFile(self.BCONTENT)),
                '%s' % self.SHA1SUM
            )
            self.assertEqual(
                storage._get_content_name(name='',
                                          content=ContentFile(self.BCONTENT),
                                          chunk_size=1),
                '%s' % self.SHA1SUM
            )
            self.assertEqual(
                storage._get_content_name(name='foo',
                                          content=ContentFile(self.BCONTENT)),
                '%s' % self.SHA1SUM
            )
            self.assertEqual(
                storage._get_content_name(name='foo.txt',
                                          content=ContentFile(self.BCONTENT)),
                '%s.txt' % self.SHA1SUM
            )
            self.assertEqual(
                storage._get_content_name(name='foo/bar',
                                          content=ContentFile(self.BCONTENT)),
                'foo/%s' % self.SHA1SUM
            )
            self.assertEqual(
                storage._get_content_name(name='foo/bar.txt',
                                          content=ContentFile(self.BCONTENT)),
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
            self.assertEqual(
                storage._compute_hash(content=ContentFile(self.BCONTENT)),
                self.SHA1SUM
            )
            self.assertEqual(
                storage._compute_hash(content=ContentFile(self.BCONTENT),
                                      chunk_size=1),
                self.SHA1SUM
            )

    def test_get_available_name_overridden_on_save(self):
        with media_root():
            storage = HashedFilenameFileSystemStorage()
            # get_available_name returns the filename given, but is overridden
            # on save
            self.assertEqual(
                storage.get_available_name('foo/bar.txt'), 'foo/bar.txt'
            )
            name1 = storage.save('foo/bar.txt', ContentFile(self.CONTENT))
            self.assertEqual(name1, 'foo/%s.txt' % self.SHA1SUM)
            self.assertEqual(storage.open(name1, 'rt').read(), self.CONTENT)

            self.assertTrue(
                os.path.exists(
                    os.path.join(settings.MEDIA_ROOT, 'foo/%s.txt' % self.SHA1SUM)
                )
            )
            self.assertFalse(
                os.path.exists(os.path.join(settings.MEDIA_ROOT, 'foo/bar.txt'))
            )

    def test_save(self):
        with media_root():
            storage = HashedFilenameFileSystemStorage()
            name1 = storage.save('foo/bar.txt', ContentFile(self.CONTENT))

            self.assertEqual(name1, 'foo/%s.txt' % self.SHA1SUM)
            self.assertEqual(storage.open(name1, 'rt').read(), self.CONTENT)

            storage.delete(name1)
            name2 = storage.save('foo/bar.txt', ContentFile(self.CONTENT))
            self.assertEqual(name2, name1)
            self.assertEqual(storage.open(name2, 'rt').read(), self.CONTENT)

            name3 = storage.save('foo/another.txt', ContentFile(self.CONTENT))
            self.assertEqual(name3, name1)
            self.assertEqual(storage.open(name3, 'rt').read(), self.CONTENT)

    def test_save_bytes_content(self):
        with media_root():
            storage = HashedFilenameFileSystemStorage()
            name1 = storage.save('foo/bar.txt', ContentFile(self.BCONTENT))
            self.assertEqual(name1, 'foo/%s.txt' % self.SHA1SUM)
            self.assertEqual(storage.open(name1, 'rb').read(), self.BCONTENT)

            storage.delete(name1)
            name2 = storage.save('foo/bar.txt', ContentFile(self.BCONTENT))
            self.assertEqual(name2, name1)
            self.assertEqual(storage.open(name2, 'rb').read(), self.BCONTENT)

            name3 = storage.save('foo/another.txt', ContentFile(self.BCONTENT))
            self.assertEqual(name3, name1)
            self.assertEqual(storage.open(name3, 'rb').read(), self.BCONTENT)


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
