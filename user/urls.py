# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login-activity/', UserLoginActivityView.as_view(), name='login-activity'),
    path('user-activity/<str:username>/', UserActivityView.as_view(), name='user-activity'),
]