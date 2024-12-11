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

# settings.py
ZOOM_API_KEY = 'ksfAaQaTRAuuzqYwJXA1VQ'
ZOOM_API_SECRET = '1LU3KX7isfl2PgbQnIRrbywbHIUbK62n'

SWAGGER_SETTINGS = {
    'USE_HTTPS': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    },
    'schemes': ['https'],
}