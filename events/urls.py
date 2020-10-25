from django.urls import path



from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventsView.as_view(), name = 'events'),
    path("<int:pk>/",views.DetailView.as_view(),name='detail'),
    path('<int:post_id>/',views.DetailView.as_view(), name='detail'),
]