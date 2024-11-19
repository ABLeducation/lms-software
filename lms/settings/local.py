from .base import *

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lms',
        'USER': 'postgres',
        'PASSWORD': 'thinnkware',
        'HOST': 'localhost',
        'PORT': '',
    }
}