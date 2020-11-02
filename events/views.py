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

    def get(self, request):
        form = EventForm()
        posts = Post.objects.all()
        query = request.GET.get("search_query")  #for searching
        if query:
            posts = posts.filter(name__icontains=query)
        args = {'form': form, 'posts': posts}
        return render(request, self.template_name, args)
        
    def post(self, request):
        if user.is_authenticated:
            form = EventForm(request.POST)
            posts = Post.objects.all()
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                form = EventForm()
        
        args = {'form': form, 'posts': posts}
        return render(request, self.template_name, args)

class DetailView(generic.DetailView):
    model = Post
    template_name = 'events/detail.html'
    def get_queryset(self):
        return Post.objects.all()
    
