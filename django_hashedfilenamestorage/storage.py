from errno import EEXIST
import hashlib
import os

from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import force_unicode
import uuid


def HashedFilenameMetaStorage(storage_class):
    class HashedFilenameStorage(storage_class):
        def __init__(self, *args, **kwargs):
            # Try to tell storage_class not to uniquify filenames.
            # This class will be the one that uniquifies.
            try:
                new_kwargs = dict(kwargs, uniquify_names=False)
                super(HashedFilenameStorage, self).__init__(*args,
                                                            **new_kwargs)
            except TypeError:
                super(HashedFilenameStorage, self).__init__(*args, **kwargs)

        def get_available_name(self, name):
            dir_name, file_name = os.path.split(name)
            file_ext = os.path.splitext(file_name)[1]

            return os.path.join(dir_name, '%s.%s' % (uuid.uuid4(), file_ext))

        def _get_content_name(self, name, content, chunk_size=None):
            dir_name, file_name = os.path.split(name)
            file_ext = os.path.splitext(file_name)[1]
            file_root = self._compute_hash(content=content,
                                           chunk_size=chunk_size)
            # file_ext includes the dot.
            return os.path.join(dir_name, file_root + file_ext)

        def _compute_hash(self, content, chunk_size=None):
            if chunk_size is None:
                chunk_size = getattr(content, 'DEFAULT_CHUNK_SIZE',
                                     File.DEFAULT_CHUNK_SIZE)

            hasher = hashlib.sha1()

            cursor = content.tell()
            content.seek(0)
            try:
                while True:
                    data = content.read(chunk_size)
                    if not data:
                        break
                    hasher.update(data)
                return hasher.hexdigest()
            finally:
                content.seek(cursor)

        def save(self, name, content, max_length=None):
            # Get the proper name for the file, as it will actually be saved.
            if name is None:
                name = content.name

            name = self._get_content_name(name, content)
            name = self._save(name, content)

            # Store filenames with forward slashes, even on Windows
            return force_unicode(name.replace('\\', '/'))

        def _save(self, name, content, *args, **kwargs):
            new_name = self._get_content_name(name=name, content=content)
            try:
                return super(HashedFilenameStorage, self)._save(new_name,
                                                                content,
                                                                *args,
                                                                **kwargs)
            except NoAvailableName:
                # File already exists, so we can safely do nothing
                # because their contents match.
                pass
            except OSError, e:
                if e.errno == EEXIST:
                    # We have a safe storage layer and file exists.
                    pass
                else:
                    raise
            return new_name

    HashedFilenameStorage.__name__ = 'HashedFilename' + storage_class.__name__
    return HashedFilenameStorage


HashedFilenameFileSystemStorage = HashedFilenameMetaStorage(
    storage_class=FileSystemStorage,
)
