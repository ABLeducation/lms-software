# Generated by Django 5.1 on 2024-12-12 09:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_alter_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivity1',
            name='content_time_spent',
            field=models.DurationField(blank=True, default=datetime.timedelta, null=True),
        ),
        migrations.AddField(
            model_name='useractivity1',
            name='quiz_time_spent',
            field=models.DurationField(blank=True, default=datetime.timedelta, null=True),
        ),
        migrations.AddField(
            model_name='useractivity1',
            name='video_time_spent',
            field=models.DurationField(blank=True, default=datetime.timedelta, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('student', 'student'), ('school', 'school'), ('teacher', 'teacher')], max_length=10),
        ),
    ]
