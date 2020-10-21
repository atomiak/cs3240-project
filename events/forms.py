from django import forms
from events.models import Post

class EventForm(forms.ModelForm):
    post = forms.CharField()

    class Meta:
        model = Post
        fields = ('post', 'date', 'date_of', 'event_description',)

