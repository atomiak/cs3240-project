from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.
from django.views import generic
from .models import EventFiller

class EventsView(generic.ListView):
    template_name = 'events/index.html'

    def get_queryset(self):
        return EventFiller.objects
        