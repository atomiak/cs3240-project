from django.urls import path



from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventsView.as_view(), name = 'events'),
    path('create/', views.CreateView.as_view(), name = 'create'),
    path("<int:pk>/",views.DetailView.as_view(),name='detail'),
    path("<int:pk>/edit/", views.EditView.as_view(), name='edit'),
    path("<int:pk>/delete/", views.delete, name='delete'),
]