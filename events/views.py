from django.shortcuts import render, redirect
from django.contrib.auth import logout
from events.forms import EventForm
from events.models import Post
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.urls import reverse
# Create your views here.
from django.views import generic
from .models import EventFiller, Post
from django.contrib.auth.decorators import login_required


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
        if request.user.is_authenticated:
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
    template_name = 'events/detail.html'

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        args = {'post': post}
        return render(request, self.template_name, args)
        
    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        if request.user.is_authenticated:
            if request.user in post.attendees.all():
                post.attendees.remove(request.user)
                request.user.past_events.remove(post)
            else:
                post.attendees.add(request.user)
                request.user.past_events.add(post)
            
        return redirect(reverse('events:events'))
    
class EditView(generic.DetailView):
    template_name = 'events/edit.html'

    def get(self, request, pk):
    
        post = Post.objects.get(pk=pk)
        if request.user.is_authenticated and request.user == post.user:
            form = EventForm(instance=post)
            args = {'form': form}
            return render(request, self.template_name, args)
        return redirect('/accounts/google/login?process=login')
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        if request.user.is_authenticated and request.user == post.user:
            form = EventForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
        else:
            return redirect('/accounts/google/login?process=login')
        return redirect(reverse('events:detail', args=[pk]))
    