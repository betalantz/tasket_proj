# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..user_app.models import User
from datetime import datetime
from dateutil.parser import parse
from django.utils import timezone
import pytz

class TaskManager(models.Manager):
    def taskValidator(self, req, postData):
        results = {'status': True, 'errors': []}
        dt_obj = parse(postData['date'])
        aware_obj = make_utc(dt_obj)
        print aware_obj
        if not postData['task'] or len(postData['task']) < 1:
            results['errors'].append('Task must be at least 1 character long.')

        if not aware_obj:
            results['errors'].append("'Date' is a required field.")

        # if not postData['time'] or len(postData['time']) < 1:
        #     results['errors'].append("'Time' is a required field.")
        
        if len(results['errors']):
            results['status']=False

        if results['status'] == True:
            # currUser = User.objects.get(id=req.session['auth_id'])
            if len(self.filter(date=aware_obj)) == 0:
                self.createTask(req, postData)
            else:
                results['errors'].append('That time is not available.')
                results['status']=False

        return results

    def createTask(self, req, postData):
        currUser = User.objects.get(id=req.session['auth_id'])
        dt_obj = parse(postData['date'])
        aware_obj = make_utc(dt_obj)
        task = Task.objects.create(
            task=postData['task'],
            status=postData['status'],
            date=aware_obj,
            # time=postData['time'],
            user=currUser
        )
        return task

def make_utc(dt):
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt)
    return dt.astimezone(pytz.utc)

class Task(models.Model):
    TASK_STATUS = (
        ('P', 'Pending'),
        ('D', 'Done'),
        ('M', 'Missed'),
    )
    task = models.TextField()
    user = models.ForeignKey(User, related_name='tasks')
    status = models.CharField(max_length=1, choices=TASK_STATUS)
    date = models.DateTimeField()
    # time = models.TextField()
    objects = TaskManager()