# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..user_app.models import User

class TaskManager(models.Manager):
    def createTask(self, postData):
        currUser = User.objects.get(id=request.session['logged_id'])
        task = Task.objects.create(
            task=postData['task'],
            status=postData['status'],
            date=postData['date'],
            time=postData['time'],
            user=currUser
        )

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
    time = models.TimeField()
    objects = TaskManager()