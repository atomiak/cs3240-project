from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Filler

class IndexView(generic.ListView):
    template_name = 'home/index.html'

    def get_queryset(self):
        return Filler.objects