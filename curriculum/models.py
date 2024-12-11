from django.db import models
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField # type: ignore
# from django.contrib.auth.models import User
from user.models import CustomUser,Student
import os
from django.urls import reverse

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug =AutoSlugField(populate_from=name,unique=True,null=True)
    class Meta:
        verbose_name_plural = '1. Schools'
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
class Standard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from=name,unique=True,null=True, default=None)
    
    class Meta:
        verbose_name_plural = '1. Standard'

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) 
        super().save(*args, **kwargs)

def save_subject_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.subject_id:
        filename = 'Subject_Pictures/{}.{}'.format(instance.subject_id, ext)
    return os.path.join(upload_to, filename)

class Subject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='subjects')
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='Subject Image')
    description = models.TextField(max_length=500,blank=True)
    display_on_frontend = models.BooleanField(default=True, verbose_name="Display on Frontend")
    schools = models.ManyToManyField(School)
    
    class Meta:
        verbose_name_plural = '2. Subjects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        

def save_lesson_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.lesson_id:
        filename = 'lesson_files/{}/{}.{}'.format(instance.lesson_id,instance.lesson_id, ext)
        if os.path.exists(filename):
            new_name = str(instance.lesson_id) + str('1')
            filename =  'lesson_images/{}/{}.{}'.format(instance.lesson_id,new_name, ext)
    return os.path.join(upload_to, filename)

class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    Standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(null=True, blank=True, unique=True)
    schools = models.ManyToManyField(School)
    tutorial_video = models.URLField(verbose_name="Videos", max_length=300, default="", null=True, blank=True)
    hint = models.FileField(upload_to=save_lesson_files, verbose_name="Hint", blank=True)
    quiz = models.URLField(verbose_name="Quiz", max_length=300, default="", null=True, blank=True)
    content = models.URLField(verbose_name="Learning Aids", max_length=300, default="", null=True, blank=True)
    editor = models.URLField(verbose_name="Editor", max_length=300, default="", null=True, blank=True)
    display_on_frontend = models.BooleanField(default=True, verbose_name="Display on Frontend")
    mark_as_completed=models.BooleanField(verbose_name="Mark as completed",default=False)

    class Meta:
        ordering = ['position']
        verbose_name_plural = '3. Lessons'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Automatically generate slug from name before saving."""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the URL to access the lesson detail view."""
        return reverse('curriculum:lesson_list', kwargs={'slug': self.subject.slug, 'standard': self.Standard.slug})

        
    
def save_mechanzo_file(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.kit_id:
        filename = 'Mechanzo_File/{}.{}'.format(instance.kit_id, ext)
    return os.path.join(upload_to, filename)
    
class Mechanzo_kit_name(models.Model):
    kit_id=models.CharField(max_length=50)
    kit_name=models.CharField(max_length=50)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.kit_name

class Mechanzo_model_name(models.Model):
    model_id=models.CharField(max_length=50)
    model_name=models.CharField(max_length=50)
    kit=models.ForeignKey(Mechanzo_kit_name, on_delete=models.CASCADE, related_name='mechanzo_models')
    slug = models.SlugField(null=True, blank=True)
    file=models.FileField(upload_to=save_mechanzo_file,verbose_name="Mechanzo", blank=True)

    def __str__(self):
        return self.model_name
        
    
class LectureRating(models.Model):
    lecture = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    date_rated = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lecture', 'user')
        

class TeacherSubject(models.Model):
    LEVEL_CHOICES = [
        ('Phase-I', 'Phase I'),
        ('Phase-II', 'Phase II'),
        ('Phase-III', 'Phase III'),
    ]
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='Subject Image')
    description = models.TextField(max_length=500,blank=True)
    display_on_frontend = models.BooleanField(default=True, verbose_name="Display on Frontend")
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name='Level',blank=True,null=True)
    
    class Meta:
        verbose_name_plural = '2. Teacher Subjects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)

class TeacherLesson(models.Model):
    MODULE_CHOICES = [
        ('Module 1', 'Module 1'),
        ('Module 2', 'Module 2'),
        ('Module 3', 'Module 3'),
    ]
    lesson_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(TeacherSubject, on_delete=models.CASCADE,related_name='Teacher_lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(null=True, blank=True)
    video=models.URLField(verbose_name="Videos", max_length=300,default="",null=True,blank=True)
    assessment=models.URLField(verbose_name="Assessment", max_length=300,default="",null=True,blank=True)
    display_on_frontend = models.BooleanField(default=True, verbose_name="Display on Frontend")
    module = models.CharField(max_length=10, choices=MODULE_CHOICES, verbose_name='Module',blank=True,null=True)

    class Meta:
        ordering = ['position']
        verbose_name_plural = '3. Teacher Lessons'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class UserLessonProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(TeacherLesson, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name_plural = '4. User Lesson Progress'

    def __str__(self):
        return f'{self.user.username} - {self.lesson.name}'      
    
class LessonAccessReport(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    video_time_spent = models.DurationField(null=True,blank=True)  # Time spent on the video
    hint_time_spent = models.DurationField(null=True,blank=True)  # Time spent on the hint
    content_time_spent = models.DurationField(null=True,blank=True)  # Time spent on the lesson content
    completed = models.BooleanField(default=False)  # Mark as completed
    accessed_at = models.DateTimeField(auto_now_add=True)  # Time of access
    updated_at = models.DateTimeField(auto_now=True)  # Last updated time

    def __str__(self):
        return f"{self.user.username} - {self.lesson.name}"