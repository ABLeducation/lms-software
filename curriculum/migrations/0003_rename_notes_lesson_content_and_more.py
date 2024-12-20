# Generated by Django 5.1 on 2024-09-27 06:42

import curriculum.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0002_alter_lesson_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='notes',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='video',
            new_name='tutorial_video',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='assessment',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='prerequisite',
        ),
        migrations.AddField(
            model_name='lesson',
            name='hint',
            field=models.FileField(blank=True, upload_to=curriculum.models.save_lesson_files, verbose_name='Hint'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='mark_as_completed',
            field=models.BooleanField(default=False, verbose_name='Mark as completed'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='quiz',
            field=models.URLField(blank=True, default='', max_length=300, null=True, verbose_name='Quiz'),
        ),
    ]
