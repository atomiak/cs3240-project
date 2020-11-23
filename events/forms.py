from django import forms
from events.models import Post
from django.core.exceptions import ValidationError

class EventForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('name', 'description', 'category', 'latitude', 'longitude', 'event_date',)
        widgets = {
            'event_date': forms.DateTimeInput(format=('%m/%d/%Y %H:%M'), attrs={'class': 'form-control', 'placeholder': 'Select a date and time', 'type':'datetime-local'}),
        }

