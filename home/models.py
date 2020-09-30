from django.db import models

# Create your models here.
import datetime
from django.utils import timezone

class Filler(models.Model):
    date = models.DateTimeField('date')