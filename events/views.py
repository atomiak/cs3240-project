from django.shortcuts import render, redirect
from django.contrib.auth import logout
from events.forms import EventForm
from events.models import Post

# Create your views here.
from django.views import generic
from .models import EventFiller

class EventsView(generic.ListView):
    template_name = 'events/index.html'

    def get_queryset(self):
        return EventFiller.objects

    
   # def get_queryset(self):
   #     return Filler.objects
    def get(self, request):
        form = EventForm()
        posts = Post.objects.all()

        args = {'form': form, 'posts': posts}
        return render(request, self.template_name, args)
        
    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            text = form.cleaned_data['post']
            form = EventForm()
            #after submitting, should redirect to the page with the list of all events, currently not working, user can manually reenter the url at the address bar to make it show up
            #return redirect('events: index') 
        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)

        
