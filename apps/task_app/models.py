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
        
        if not postData['task'] or len(postData['task']) < 1:
            results['errors'].append('Task must be at least 1 character long.')

        if not postData['date'] or len(postData['date']) < 1:
            results['errors'].append("'Date' is a required field.")

        if len(results['errors']):
            results['status']=False

        if results['status'] == True:
            dt_obj = parse(postData['date'])
            aware_obj = make_utc(dt_obj)
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
            user=currUser
        )
        return task

def make_utc(dt):
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt)
    return dt.astimezone(pytz.utc)

class Task(models.Model):
    TASK_STATUS = (
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    )
    task = models.TextField()
    user = models.ForeignKey(User, related_name='tasks')
    status = models.CharField(max_length=1, choices=TASK_STATUS)
    date = models.DateTimeField()
    objects = TaskManager()