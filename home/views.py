from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.
from django.views import generic
from .models import Filler

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from events.forms import EventForm
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

    def get(self, request):
        form = EventForm()
        posts = Post.objects.all()
        args = {posts: posts}
        return render(request, self.template_name, args)