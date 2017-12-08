SECRET_KEY = "test-secret"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
    }
}

INSTALLED_APPS = [
    'django_hashedfilenamestorage',
]

DEFAULT_FILE_STORAGE = 'django_hashedfilenamestorage.storage.HashedFilenameFileSystemStorage'
