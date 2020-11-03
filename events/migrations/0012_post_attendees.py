# Generated by Django 3.1.1 on 2020-11-03 01:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0011_auto_20201101_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='attendees',
            field=models.ManyToManyField(related_name='past_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
