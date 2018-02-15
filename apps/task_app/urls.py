from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    
    url(r'^$', views.display_dash),
    url(r'^edit/(?P<task_id>\d+)/$', views.editTask, name='edit'),
    url(r'^update/(?P<task_id>\d+)/$', views.updateTask, name='update'),
    url(r'^delete/(?P<task_id>\d+)/$', views.deleteTask, name='delete'),
    url(r'^add/$', views.addTask, name='add'),
]