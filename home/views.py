
# REFERENCES
# Title: Django-allauth
# Author: Raymond Penners Revision
# Date: Copyrigh 2017, Accessed 10/5/2020
# URL: https://django-allauth.readthedocs.io/en/latest/
# Software License: BSD 3

from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.
from django.views import generic
from .models import Filler

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from events.forms import EventForm
from django.contrib.auth.models import User
from events.models import Post
from django.http import HttpResponseRedirect
from django.views.generic import CreateView

# Create your views here.
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'home/index.html'

    def get_queryset(self):
        return Filler.objects


def pagelogout(request):
    logout(request)
    return redirect('home:index')

class ProfileView(generic.ListView):
    template_name = 'home/profile.html'

    def get(self, request, pk):
        if not request.user.is_authenticated or request.user.id != pk:
            return redirect('/accounts/google/login?process=login')
        user = User.objects.get(id=pk)
        posts = Post.objects.filter(user=user)
        past_events = user.past_events.all()
        args = {'posts': posts, 'user' : user, 'past_events' : past_events}
        return render(request, self.template_name, args)