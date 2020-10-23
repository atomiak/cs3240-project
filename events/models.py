from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import datetime
from django.utils import timezone

class EventFiller(models.Model):
    date = models.DateTimeField('date')

class Post(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    # different categories- this code might be not as efficient as possible but it works
    party = 'Party'
    study = 'Study Session'
    sports = 'Athletic Event'
    category_choices = [
        (party, party),
        (study, study),
        (sports, sports),
    ]
    category = models.CharField(max_length=50, choices=category_choices, default=party)
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    date = models.DateTimeField(verbose_name = "Date of creation", default=timezone.now, null=False)
    xcoordinate = models.CharField(max_length=500)
    ycoordinate = models.CharField(max_length=500)

