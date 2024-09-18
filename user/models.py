from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# User=get_user_model()

# Create your models here.
class CustomUser(AbstractUser):
    Role_Choices={
        ('student','student'),
        ('teacher','teacher'),
        ('school','school')
    }
    role=models.CharField(max_length=10,choices=Role_Choices)
    
class Student(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    name=models.CharField(max_length=50)
    grade=models.CharField(max_length=50)
    section=models.CharField(max_length=50)
    school=models.CharField(max_length=200)
    
    class Meta:
        verbose_name = 'Student'

    def __str__(self):
        return self.user.username
    
class Teacher(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    school=models.CharField(max_length=200)
    
class School(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    school=models.CharField(max_length=200)