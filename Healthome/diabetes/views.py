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
	if request.method == 'POST':
		if "add" in request.POST:
			board_no = request.POST['add_board']
			new_board = ArduinoBoard(
					user=user,
					board=board_no,
					used='True'
				)
			new_board.save()
		elif "delete" in request.POST:
			board_no = request.POST['delete_board']
			ArduinoBoard.objects.filter(user=user, board=board_no).delete()
		return HttpResponseRedirect('/diabetes/profile/')
	arduino = ArduinoBoard.objects.filter(user=user)
	context = {
		"user": user,
		"tag": "profile",
		"boards": arduino,
	}
	return render(request, "profile.html", context)

def input(request):
	user_id = request.session['user_id']
	user = User.objects.get(pk=user_id)
	if InputBodyStatus.objects.filter(user=user).exists():
		body_status = InputBodyStatus.objects.filter(user=user).order_by('-id')[0]
		context = {
			"user": user,
			"tag": "input",
			"status": body_status,
		}
		return render(request, "input.html", context)
	if request.method == 'POST':
		new_satuts = InputBodyStatus(
				user=user,
				pregnant=request.POST['pregnant'],
				skinfold=request.POST['skinfold'],
				seruminsulin=request.POST['seruminsulin'],
				bmi=request.POST['bmi'],
				pedigree=request.POST['pedigree'],
				age=request.POST['age'],
			)
		new_satuts.save()
		body_status = InputBodyStatus.objects.filter(user=user).order_by('-id')[0]
		context = {
			"user": user,
			"tag": "input",
			"status": body_status,
			"message": "Body status saved successfully!",
		}
		return render(request, "input.html", context)
	context = {
			"user": user,
			"tag": "input",
		}
	return render(request, "input.html", context)

def arduino(request):
	return render(request, "arduino.html")

def result(request):
	return render(request, "result.html")