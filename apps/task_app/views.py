# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.utils import timezone
from ..user_app.views import sessionCheck
import datetime
from dateutil.parser import parse
import pytz
from models import Task


def display_dash(req):
    if sessionCheck(req) == False:
        messages.warning(req, 'Please login to access tasks.')
        return redirect('/')
    today = timezone.now()
    context = {
        'today': timezone.localtime(today).date,
        'curr_tasks': Task.objects.filter(user_id=req.session['auth_id']).filter(date__year=timezone.localtime(timezone.now()).year).filter(date__month=timezone.localtime(timezone.now()).month).filter(date__day=timezone.localtime(timezone.now()).day).order_by('date'),
        'future_tasks': Task.objects.filter(user_id=req.session['auth_id']).filter(date__gt=timezone.localtime(timezone.now())).exclude(date__day=timezone.localtime(timezone.now()).day).order_by('date'),
        # 'addForm': NewTask()
    }
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
        dt_obj = parse(req.POST['date'])
        aware_obj = make_utc(dt_obj)
        update.date = aware_obj
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

def make_utc(dt):
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt)
    return dt.astimezone(pytz.utc)