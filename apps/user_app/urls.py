from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^register/$', views.process_reg, name='register'),
    url(r'^login/$', views.process_log, name='login'),
    url(r'^', views.process_reg),
]