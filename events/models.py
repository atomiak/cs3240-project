from django.db import models

# Create your models here.
import datetime
from django.utils import timezone

class EventFiller(models.Model):
    date = models.DateTimeField('date')

class Event(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date')
