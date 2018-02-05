# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..user_app.views import sessionCheck
import datetime
from models import Task
from forms import NewTask

# def test(req):
#     res='Welcome to user_app views'
#     return render(req, 'task_app/dash.html')

def display_dash(req):
    if sessionCheck(req) == False:
        messages.warning(req, 'Please login to access tasks.')
        return redirect('/')

    context = {
        'today': datetime.date.today(),
        'curr_tasks': Task.objects.filter(user=req.session['auth_id']).filter(date=datetime.date.today()),
        'future_tasks': Task.objects.filter(user=req.session['auth_id']).filter(date__gt=datetime.date.today()),
        'addForm': NewTask()
    }
    return render(req, 'task_app/dash.html', context)

def editTask(req):
    pass

def deleteTask(req):
    pass
    
def addTask(req):
    pass