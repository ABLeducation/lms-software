from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
import os
# User=get_user_model()

# Create your models here.
class CustomUser(AbstractUser):
    Role_Choices={
        ('student','student'),
        ('teacher','teacher'),
        ('school','school')
    }
    role=models.CharField(max_length=10,choices=Role_Choices)
    email = models.EmailField(unique=True)
    
def student_profile_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.user:
        filename = 'Student_Pictures/{}.{}'.format(instance.user, ext)
    return os.path.join(upload_to, filename)
    
class Student(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    name=models.CharField(max_length=50)
    grade=models.CharField(max_length=50)
    section=models.CharField(max_length=50)
    school=models.CharField(max_length=200)
    profile_pic=models.ImageField(upload_to=student_profile_image, blank=True, verbose_name='Profile Image')
    
    class Meta:
        verbose_name = 'Student'

    def __str__(self):
        return self.user.username
    
GRADES = [
    ('grade_1', 'Grade 1'),
    ('grade_2', 'Grade 2'),
    ('grade_3', 'Grade 3'),
    ('grade_4', 'Grade 4'),
    ('grade_5', 'Grade 5'),
    ('grade_6', 'Grade 6'),
    ('grade_7', 'Grade 7'),
    ('grade_8', 'Grade 8'),
    ('grade_9', 'Grade 9'),
    ('grade_10', 'Grade 10'),
    ('grade_11', 'Grade 11'),
    ('grade_12', 'Grade 12'),
]
   
class Teacher(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    school=models.CharField(max_length=200)
    name=models.CharField(max_length=100,default="")
    mobile_num = models.CharField(
        max_length=10, 
        null=True, 
        blank=True, 
        validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits")]
    )
    subject=models.CharField(max_length=20,null=True,blank=True)
    designation=models.CharField(max_length=20,null=True)
    grades = models.CharField(
        max_length=200,
        choices=GRADES,
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return self.name
    
class School(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    school=models.CharField(max_length=200)
    city=models.CharField(max_length=50,null=True)
    state=models.CharField(max_length=50,null=True)
    country=models.CharField(max_length=100,null=True)
    principal_name=models.CharField(max_length=100,default="")
    principal_number=models.CharField(
        max_length=10, 
        null=True, 
        blank=True, 
        validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits")]
    )
    principal_email=models.CharField(max_length=100, blank=True)
    teacher_coordinator = models.CharField(max_length=500, null=True, blank=True, help_text="Enter multiple coordinators separated by commas.")
    teacher_coordinator_number=models.CharField(max_length=100,null=True)
    teacher_coordinator_email=models.CharField(max_length=100,null=True)
    accountant_number=models.CharField(
        max_length=10, 
        null=True, 
        blank=True, 
        validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits")]
    )
    account_name=models.CharField(max_length=100, blank=True)
    account_email=models.CharField(max_length=100, blank=True)
    geo_location = models.CharField(max_length=100, null=True, blank=True, help_text="Format: latitude,longitude")
    
    def __str__(self):
        return self.school

    
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
    
    
class Macroplanner(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    grade=models.CharField(max_length=100,null=True,blank=True)
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    macroplanner=models.FileField(upload_to='macroplanner/')
    
    def __str__(self):
        return f"Macroplanner - User: {self.user.username}, File: {self.macroplanner.name}"
    
class Microplanner(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    month=models.CharField(max_length=100,default="")
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global SChool,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    microplanner=models.FileField(upload_to='microplanner/')
    
    def __str__(self):
        return f"Microplanner - User: {self.user.username}, File: {self.microplanner.name}"
    
class AdvocacyVisit(models.Model):
    name=models.CharField(max_length=100)
    grade=models.PositiveIntegerField(choices= [(i, str(i)) for i in range(1, 13)],default=1)
    section=models.CharField(max_length=1, choices=[(chr(i), chr(i)) for i in range(65, 76)],default="A")
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global SChool,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur')),default=None
        )
    date=models.DateField()
    duration=models.CharField(max_length=50)
    topics=models.CharField(max_length=100)
    topics_microplanner = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)
    classroom_management = models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    content_delievery=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )

    student_teacher_relation=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    dresscode=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    handling_comm=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    Regularity=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    Punctuality=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    daily_report=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    daily_progress_sheet=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    overall_behaviour=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    next_month_microplanner=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    kreativityshow=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    compiled_report=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    daily_win_sharing=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    photo_video_recording=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    pedagogical_poweress=models.TextField()
    additional_info=models.TextField()
    project_taken_club=models.TextField()
    learning_outcomes=models.TextField()
    competition=models.TextField()
    feedback=models.TextField()
    improvement_tips=models.TextField()
    remarks=models.TextField()
    name_advocacy=models.CharField(max_length=100)
    verified_by=models.BooleanField(default=False)
    gallery=models.URLField()

    def __str__(self):
        return self.name+' - '+self.school
    
class InnovationClub(models.Model):
    name=models.ForeignKey(Student, on_delete=models.CASCADE,null=True,blank=True)
    grade=models.CharField(max_length=100)
    section=models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(null=True, blank=True)
    project_name=models.CharField(max_length=100)
    progress=models.CharField(max_length=200)
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    
    def __str__(self):
        return f'{self.school} - {self.date}'


class Competition(models.Model):
    competition_name=models.CharField(max_length=100)
    venue=models.CharField(max_length=100)
    date=models.DateField()
    status=models.CharField(max_length=100)
    grade = models.CharField(max_length=50,null=True,blank=True)
    section = models.CharField(max_length=50,null=True,blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True,blank=True)
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )

    def __str__(self):
        return f'{self.school} - {self.date}'

class GuestSession(models.Model):
    date=models.DateField()
    guest_name=models.CharField(max_length=100)
    gallery=models.URLField()
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
        
    def __str__(self):
        return f'{self.school} - {self.date}'
    
class KreativityShow(models.Model):
    date=models.DateField()
    parent_name=models.CharField(max_length=100)
    child_name=models.CharField(max_length=100)
    testimonial=models.URLField()
    grade=models.CharField(max_length=100)
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
        
class SchoolContract(models.Model):
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Subscription for {self.school} from {self.start_date} to {self.end_date}"
        
class SchoolGallery(models.Model):
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    gallery = models.URLField()
    
    class Meta:
        verbose_name_plural = "School's Galleries"

    def __str__(self):
        return self.school
        
class ObservationSheet(models.Model):
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    observation_sheet = models.URLField()

    def __str__(self):
        return self.school
    
class CurriculumView(models.Model):
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    curriculum_sheet = models.URLField()

    def __str__(self):
        return self.school
    
class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_id.name