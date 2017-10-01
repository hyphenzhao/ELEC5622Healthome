# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from .models import *


def index(request):
	if 'user_id' in request.session:
		user = authenticate(id = request.session['user_id'])
		if user is not None:
			return HttpResponseRedirect('/diabetes/profile/')
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(username = email, password = password)
		if user is not None:
			request.session["user_id"] = user.id
			return HttpResponseRedirect('/diabetes/profile/')
		else:
			return HttpResponse("The email and password pair does not exist.")
	return render(request, "index.html")

def register(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		user = User.objects.create_user(
				username = email,
				password = password,
				email = email,
				first_name = firstname,
				last_name = lastname
			)
		return render(request, "index.html")
	return render(request, "register.html")

def profile(request):
	user_id = request.session['user_id']
	user = User.objects.get(pk=user_id)
	context = {
		"user": user,
	}
	return render(request, "profile.html", context)