# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt

class UserManager(models.Manager):
    def createUser(self, postData):
        hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            name=postData['name'],
            email=postData['email'],
            password=hash1,
            timezone=postData['timezone']
        )
        return user
    

class User(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length=50)
    timezone = models.CharField(max_length = 50, default="UTC")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return "<User object: {} {}>".format(self.name, self.email)
