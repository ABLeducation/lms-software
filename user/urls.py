# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
]
