# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import RegForm, LogForm
from models import User
import bcrypt

def process_reg(req):
    print "Hit process_reg()"
    # if this is a POST request we need to process the form data
    if req.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegForm(req.POST)
        print "form instantiated with req.POST data"
        # check whether it's valid
        if form.is_valid():
            print "form is valid"
            print form.cleaned_data
            # process the data in form.cleaned_data as required
            # Check for previously existing user
            email_matches = User.objects.filter(email=form.cleaned_data['email'])
            print email_matches
            if not len(email_matches) == 0:
                messages.error(req, 'We already have an entry with that email, with name of {}'.format(email_matches[0].name))
                return redirect('/')
            # Check that passwords match
            if not form.data['password'] == form.data['conf_pass']:
                messages.error(req, 'Passwords did not match, please re-enter.')
                return redirect('/')
            # Create and save new user
            new_user = User()
            new_user.name = form.cleaned_data['name']
            new_user.email = form.cleaned_data['email']
            hashed_pw = bcrypt.hashpw(form.cleaned_data['password'].encode(), bcrypt.gensalt())
            new_user.password = hashed_pw
            new_user.timezone = form.cleaned_data['timezone']
            messages.success(req, 'You have registered successfully. Please log in.')
            new_user.save()

            # render or redirect
            return redirect('/')
        print "form failed validation"
    # if a GET (or other method) create a blank form
    else:
        # form = RegForm()
        # log_form = LogForm()
        context = {
            'form': RegForm(),
            'log_form': LogForm()
        }

    return render(req, 'user_app/login.html', context)

def process_log(req):
    print "Hit process_log"
    # if this is POST request, process form data
    if req.method == 'POST':
        # create form instance and populate with req data
        log_form = LogForm(req.POST)
        # check if valid
        if log_form.is_valid():
            # process the data as required
            # Check that there is only one matching user in db
            num_users = len(User.objects.filter(email=log_form.cleaned_data['email']))
            if num_users > 1:
                messages.warning(req, 'There are more than one user with the email {}'.format(log_form.cleaned_data['email']))
            elif num_users == 0:
                messages.warning(req, 'Email not found.')
                return redirect('/process_log')

            # match password in db
            curr_user = User.objects.get(email=log_form.cleaned_data['email'])
            pw_auth = bcrypt.checkpw(log_form.cleaned_data['password'].encode(), curr_user.password.encode())

            # if password valid, put user in session
            if pw_auth:
                req.session['auth_id'] = curr_user.id
                req.session['auth_name'] = curr_user.name
                print "{} {} saved to session".format(req.session['auth_id'], req.session['auth_name'])
                messages.info(req, 'Login successful.')
                return redirect('/task/')
            else:
                messages.warning(req, 'Please re-enter a valid password.')
                return redirect('/process_log')

    else:
    # form = RegForm()
    # log_form = LogForm()
        context = {
            'form': RegForm(),
            'log_form': LogForm()
        }

    return render(req, 'user_app/login.html', context)

def sessionCheck(req):
    print "@ sessionCheck"
    try:
        return req.session['auth_id']
    except:
        return False

def logout(req):
    print "@ logout"
    req.session.flush()
    print "session flushed"
    storage = messages.get_messages(req)
    for message in storage:
        print(message)
    storage.used = True
    return redirect('/')