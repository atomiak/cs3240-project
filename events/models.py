from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
import datetime
from django.utils import timezone

class EventFiller(models.Model):
    date = models.DateTimeField('date')
#post is an event
class Post(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(max_length=500)
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
    longitude = models.FloatField(default=0, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    latitude = models.FloatField(default=0, validators=[MinValueValidator(-90), MaxValueValidator(180)])
    event_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    attendees = models.ManyToManyField(User, related_name='past_events')
    def name_to_text(self):
        return self.name
    def description_to_text(self):
        return self.description
    def category_to_text(self):
        return self.category
    def x_to_text(self):
        return self.longitude
    def y_to_text(self):
        return self.latitude
    def attendees_list(self):
        return self.attendees

