from django.shortcuts import render, redirect
from django.contrib.auth import logout
from events.forms import EventForm
from events.models import Post
from django.http import HttpResponseRedirect
from django.views.generic import CreateView

# Create your views here.
from django.views import generic
from .models import EventFiller, Post

class EventsView(generic.ListView):
    template_name = 'events/index.html'

    # def get_queryset(self):
    #     return EventFiller.objects

    
   # def get_queryset(self):
   #     return Filler.objects
    def get(self, request):
        form = EventForm()
        posts = Post.objects.all()

        args = {'form': form, 'posts': posts}
        return render(request, self.template_name, args)
        
    def post(self, request):
        form = EventForm(request.POST)
        posts = Post.objects.all()
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form = EventForm()
            #after submitting, should redirect to the page with the list of all events, currently not working, user can manually reenter the url at the address bar to make it show up
            #return redirect('events: index') 
        
        args = {'form': form, 'posts': posts}
        return render(request, self.template_name, args)

class DetailView(generic.DetailView):
    model = Post
    template_name = 'events/detail.html'
    def get_queryset(self):
        return Post.objects.all()
    