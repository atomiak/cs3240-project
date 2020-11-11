from django import forms
from events.models import Post

class EventForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('name', 'description', 'category', 'xcoordinate', 'ycoordinate',)

