# Generated by Django 5.1 on 2024-09-19 06:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLoginActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_IP', models.GenericIPAddressField(blank=True, null=True)),
                ('login_datetime', models.DateTimeField()),
                ('login_username', models.CharField(blank=True, max_length=40, null=True)),
                ('status', models.CharField(blank=True, choices=[('S', 'Success'), ('F', 'Failed')], default='S', max_length=1, null=True)),
                ('user_agent_info', models.CharField(max_length=255)),
                ('login_num', models.CharField(default=0, max_length=1000)),
            ],
            options={
                'verbose_name': 'User Login Activity',
                'verbose_name_plural': 'User Login Activities',
            },
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('school', 'school'), ('student', 'student'), ('teacher', 'teacher')], max_length=10),
        ),
        migrations.CreateModel(
            name='UserActivity1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('login_time', models.DateTimeField(blank=True, null=True)),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('page_visited', models.CharField(max_length=255)),
                ('curriculum_time_spent', models.DurationField(blank=True, null=True)),
                ('time_spent', models.DurationField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Acess Report',
                'verbose_name_plural': 'User Acess Reports',
            },
        ),
    ]
