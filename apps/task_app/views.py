# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

# def test(req):
#     res='Welcome to user_app views'
#     return render(req, 'task_app/dash.html')

def display_dash(req):
    try:
        int(req.session['auth_id'])
    except:
        messages.warning(req, 'Please login to access tasks.')
        return redirect('/')
    return render(req, 'task_app/dash.html')
