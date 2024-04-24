from django.urls import path

from . import views

app_name = 'hailmaps'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_hailmap, name='new_hailmap'),
    path('events/', views.hail_events, name='hail_events'),
]