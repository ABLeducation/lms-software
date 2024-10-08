# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', StandardListAPIView.as_view(), name='standard_list'),
    path('<slug:slug>/', SubjectListAPIView.as_view(), name='subject_list'),
    path('<str:standard>/<slug:slug>/', LessonListAPIView.as_view(), name='lesson_list'),
    path('<str:standard>/<str:subject>/<slug:slug>/', LessonDetailAPIView.as_view(), name='lesson_detail'),
]