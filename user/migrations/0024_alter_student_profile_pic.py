# Generated by Django 5.1 on 2024-10-09 09:46

import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_alter_customuser_role_alter_student_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to=user.models.student_profile_image, verbose_name='Profile Image'),
        ),
    ]