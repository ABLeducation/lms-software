from .base import *

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lms',
        'USER': 'postgres',
        'PASSWORD': 'Trust@786',
        'HOST': 'localhost',
        'PORT': '',
    }
}