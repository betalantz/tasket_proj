# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
# from django.utils.timezone import localtime, now
from django.utils import timezone
from ..user_app.views import sessionCheck
# import datetime
# import pytz
from models import Task
from forms import NewTask

# def test(req):
#     res='Welcome to user_app views'
#     return render(req, 'task_app/dash.html')

def display_dash(req):
    if sessionCheck(req) == False:
        messages.warning(req, 'Please login to access tasks.')
        return redirect('/')
    today = timezone.now()
    context = {
        # 'today': datetime.date.today(),
        'today': timezone.localtime(today).date,
        'curr_tasks': Task.objects.filter(user_id=req.session['auth_id']).filter(date=timezone.now()).order_by('date'),
        'future_tasks': Task.objects.filter(user_id=req.session['auth_id']).filter(date__gt=timezone.now()).order_by('date'),
        # 'curr_tasks': Task.objects.filter(user_id=req.session['auth_id']).filter(date=localtime(now())).order_by('time'),
        # 'future_tasks': Task.objects.filter(user_id=req.session['auth_id']).filter(date__gt=localtime(now())).order_by('date', 'time'),
        'addForm': NewTask()
    }
    # logged = req.session['auth_id']
    # later = Task.objects.filter(user_id=req.session['auth_id']).filter(date__gt=datetime.date.today())
    # print "filter returns:"
    # print later
    # print logged
    return render(req, 'task_app/dash.html', context)

def editTask(req, task_id):
    if sessionCheck(req) == False:
        messages.warning(req, 'Please login to access tasks.')
        return redirect('/')

    context = {
        'task': Task.objects.get(id=task_id)
    }
    return render(req, 'task_app/edit.html', context)

def updateTask(req, task_id):
    update = Task.objects.get(id = task_id)
    if req.POST['task']:
        update.task = req.POST['task']
    if req.POST['status']:
        update.status = req.POST['status']
    if req.POST['date']:
        update.date = req.POST['date']
    if req.POST['time']:
        update.time = req.POST['time']
    update.save()
    return redirect('/task/')

def addTask(req):
    results = Task.objects.taskValidator(req, req.POST)
    if results['status']==False:
        for error in results['errors']:
            messages.error(req, error)
        return redirect('/task/')
    # messages.success(req, 'Your task has been added.')
    return redirect('/task/')

def deleteTask(req, task_id):
    thisTask = Task.objects.get(id=task_id)
    thisTask.delete()
    return redirect('/task/')

def search_tasks(req):
    if req.method == 'POST':
        search_text = req.POST['search_text']
    else: 
        search_text = ''
