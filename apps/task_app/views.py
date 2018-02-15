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
        'curr_tasks': Task.objects.filter(user_id=req.session['auth_id']).filter(date=datetime.date.today()),
        'future_tasks': Task.objects.filter(user_id=req.session['auth_id']).filter(date__gt=datetime.date.today()),
        'addForm': NewTask()
    }
    logged = req.session['auth_id']
    later = Task.objects.filter(user_id=req.session['auth_id']).filter(date__gt=datetime.date.today())
    print "filter returns:"
    print later
    print logged
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