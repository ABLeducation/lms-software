from .base import *

# local.py
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']


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