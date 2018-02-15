# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..user_app.models import User

class TaskManager(models.Manager):
    def taskValidator(self, req, postData):
        results = {'status': True, 'errors': []}
 
        if not postData['task'] or len(postData['task']) < 1:
            results['errors'].append('Task must be at least 1 character long.')

        if not postData['date'] or len(postData['date']) < 1:
            results['errors'].append("'Date' is a required field.")

        if not postData['time'] or len(postData['time']) < 1:
            results['errors'].append("'Time' is a required field.")
        
        if len(results['errors']):
            results['status']=False

        if results['status'] == True:
            # currUser = User.objects.get(id=req.session['auth_id'])
            if len(self.filter(date=postData['date'], time=postData['time'])) == 0:
                self.createTask(req, postData)
            else:
                results['errors'].append('That time is not available.')
                results['status']=False

        return results

    def createTask(self, req, postData):
        currUser = User.objects.get(id=req.session['auth_id'])
        task = Task.objects.create(
            task=postData['task'],
            status=postData['status'],
            date=postData['date'],
            time=postData['time'],
            user=currUser
        )
        return task

class Task(models.Model):
    TASK_STATUS = (
        ('P', 'Pending'),
        ('D', 'Done'),
        ('M', 'Missed'),
    )
    task = models.TextField()
    user = models.ForeignKey(User, related_name='tasks')
    status = models.CharField(max_length=1, choices=TASK_STATUS)
    date = models.DateField()
    time = models.TextField()
    objects = TaskManager()