# Generated by Django 5.1 on 2024-12-10 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0004_lessonaccessreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonaccessreport',
            name='video_time_spent',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
