# Generated by Django 5.1 on 2024-09-26 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('teacher', 'teacher'), ('school', 'school'), ('student', 'student')], max_length=10),
        ),
    ]
