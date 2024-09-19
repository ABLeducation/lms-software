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
    
class UserLoginActivity(models.Model):
    # Login Status
    SUCCESS = 'S'
    FAILED = 'F'

    LOGIN_STATUS = ((SUCCESS, 'Success'),
                           (FAILED, 'Failed'))

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField()
    login_username = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=1, default=SUCCESS, choices=LOGIN_STATUS, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)
    login_num=models.CharField(max_length=1000,default=0)

    class Meta:
        verbose_name = 'User Login Activity'
        verbose_name_plural = 'User Login Activities'
        
    def get_student_name(self):
        try:
            student_profile = Student.objects.get(user__username=self.login_username)
            return f"{student_profile.name}"
        except Student.DoesNotExist:
            return None
        
    def get_grade(self):
        try:
            student_profile = Student.objects.get(user__username=self.login_username)
            grade=student_profile.grade
            return f"{grade}"
        except Student.DoesNotExist:
            return None
        
    def get_section(self):
        try:
            student_profile = Student.objects.get(user__username=self.login_username)
            section=student_profile.section
            return f"{section}"
        except Student.DoesNotExist:
            return None

    def __str__(self):
        return self.login_username
        
class UserActivity1(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    page_visited = models.CharField(max_length=255)
    curriculum_time_spent = models.DurationField(null=True, blank=True)
    time_spent = models.DurationField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'User Acess Report'
        verbose_name_plural = 'User Acess Reports'

    def __str__(self):
        return f"{self.user.username} - {self.page_visited} on {self.date}"