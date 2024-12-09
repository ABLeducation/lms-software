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

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # React dev server
    # "https://worm-dear-centrally.ngrok-free.app",
    'https://75f9-122-161-67-80.ngrok-free.app'
]

CSRF_TRUSTED_ORIGINS = [
    # 'https://worm-dear-centrally.ngrok-free.app',
    'https://75f9-122-161-67-80.ngrok-free.app'
    'http://localhost:5173']

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