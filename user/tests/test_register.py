import pytest # type: ignore
from rest_framework import status  # type: ignore
from django.urls import reverse
from rest_framework.test import APITestCase # type: ignore

@pytest.mark.django_db
def test_register_student(client):
    url = reverse('users:register')
    data = {
        "user": {
            "username": "student1",
            "password": "password123",
            "email": "student1@example.com",
            "role": "student"
        },
        "name": "Student Name",
        "grade": "Grade 5",
        "section": "A",
        "school": "School Name"
    }

    response = client.post(url, data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_register_teacher(client):
    url = reverse('users:register')
    data = {
        "user": {
            "username": "teacher1",
            "password": "password123",
            "email": "teacher1@example.com",
            "role": "teacher"
        },
        "school": "School Name"
    }

    response = client.post(url, data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_register_school(client):
    url = reverse('users:register')
    data = {
        "user": {
            "username": "school1",
            "password": "password123",
            "email": "school1@example.com",
            "role": "school"
        },
        "school": "School Name"
    }

    response = client.post(url, data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_register_invalid_role(client):
    url = reverse('users:register')
    data = {
        "user": {
            "username": "invalid1",
            "password": "password123",
            "email": "invalid1@example.com",
            "role": "invalid_role"
        }
    }

    response = client.post(url, data, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST