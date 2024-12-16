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

CORS_ALLOWED_ORIGINS = [
    'https://credible-becoming-spider.ngrok-free.app',
    'http://localhost:5173'
]

CSRF_TRUSTED_ORIGINS = [
    'https://credible-becoming-spider.ngrok-free.app',
    'http://localhost:5173',
]
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
CSRF_COOKIE_SECURE = True
SameSite=None