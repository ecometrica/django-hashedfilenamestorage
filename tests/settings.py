import os

SITE_ID = 1

TEST_ROOT = os.path.normcase(os.path.dirname(os.path.abspath(__file__)))

FIXTURES_ROOT = os.path.join(TEST_ROOT, 'fixtures')

MEDIA_ROOT = os.path.join(TEST_ROOT, 'media')
MEDIA_URL = '/media/'

DATABASE_ENGINE = 'sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'tests',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

# This is only needed for the 1.4.X test environment
USE_TZ = True

SECRET_KEY = 'easy'

###############################################################


DEFAULT_FILE_STORAGE = 'django_hashedfilenamestorage.storage.HashedFilenameFileSystemStorage'
