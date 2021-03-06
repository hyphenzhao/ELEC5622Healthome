# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from .models import *
from services import *


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
		user.save()
		return HttpResponseRedirect('/diabetes/')
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
	if request.method == 'POST':
		new_input_satuts = InputBodyStatus(
				user=user,
				pregnant=request.POST['pregnant'],
				skinfold=request.POST['skinfold'],
				seruminsulin=request.POST['seruminsulin'],
				bmi=request.POST['bmi'],
				pedigree=request.POST['pedigree'],
				age=request.POST['age'],
			)
		new_input_satuts.save()
		body_status = InputBodyStatus.objects.filter(user=user).order_by('-id')[0]
		context = {
			"user": user,
			"tag": "input",
			"status": body_status,
			"message": "Body status saved successfully!",
		}
		return render(request, "input.html", context)
	if InputBodyStatus.objects.filter(user=user).exists():
		body_status = InputBodyStatus.objects.filter(user=user).order_by('-id')[0]
		context = {
			"user": user,
			"tag": "input",
			"status": body_status,
		}
		return render(request, "input.html", context)
	context = {
			"user": user,
			"tag": "input",
		}
	return render(request, "input.html", context)

def arduino(request):
	if (request.method == 'GET') and ("arduino_board_no" in request.GET) and (request.GET["arduino_board_no"]!=""):
		arduino_board = ArduinoBoard.objects.filter(board=request.GET["arduino_board_no"]).order_by('-id')[0]
		user = arduino_board.user
		body_status_list = TestBodyStatus.objects.filter(user=user)
		if body_status_list:
			if("bloodpressure" not in request.GET):
				bloodpressure = body_status_list.order_by('-id')[0].bloodpressure
			else:
				bloodpressure = request.GET['bloodpressure']
			if("glucose" not in request.GET):
				glucose = body_status_list.order_by('-id')[0].glucose
			else:
				glucose = request.GET['glucose']
		else:
			if("bloodpressure" not in request.GET):
				bloodpressure = 0
			else:
				bloodpressure = request.GET['bloodpressure']
			if("glucose" not in request.GET):
				glucose = 0
			else:
				glucose = request.GET['glucose']
		new_test_satuts = TestBodyStatus(
				user=user,
				glucose=glucose,
				bloodpressure=bloodpressure
			)	
		new_test_satuts.save()
		return HttpResponse("Save successfully!");
	user_id = request.session['user_id']
	user = User.objects.get(pk=user_id)
	if request.method == 'POST':
		new_test_satuts = TestBodyStatus(
				user=user,
				glucose=request.POST['glucose'],
				bloodpressure=request.POST['bloodpressure']
			)
		new_test_satuts.save()
		body_status = TestBodyStatus.objects.filter(user=user).order_by('-id')[0]
		context = {
			"user": user,
			"tag": "arduino",
			"status": body_status,
			"message": "Arduino Board test result got successfully!",
		}
		return render(request, "arduino.html", context)
	if TestBodyStatus.objects.filter(user=user).exists():
		body_status = TestBodyStatus.objects.filter(user=user).order_by('-id')[0]
		context = {
			"user": user,
			"tag": "arduino",
			"status": body_status,
		}
		return render(request, "arduino.html", context)
	context = {
			"user": user,
			"tag": "arduino",
		}
	return render(request, "arduino.html", context)

def result(request):
	user_id = request.session['user_id']
	user = User.objects.get(pk=user_id)
	if request.method == 'POST':
		if "add" in request.POST:
			i = InputBodyStatus.objects.filter(user=user).order_by('-id')[0]
			t = TestBodyStatus.objects.filter(user=user).order_by('-id')[0]
			testpoint = [i.pregnant,t.glucose,t.bloodpressure,i.skinfold,i.seruminsulin,i.bmi,i.pedigree,i.age]
			r = calculate_probability(testpoint)
			new_result = TestResult(
					user=user,
					inputstatus=i,
					teststatus=t,
					result=r,
				)
			new_result.save()
		elif "delete" in request.POST:
			record_id = request.POST['recordID']
			TestResult.objects.get(pk=record_id).delete()
	test_result = TestResult.objects.filter(user=user).order_by('-id')
	arduino_status = TestBodyStatus.objects.filter(user=user)
	input_status = InputBodyStatus.objects.filter(user=user)
	if arduino_status and input_status:
		context = {
			"user": user,
			"tag": "result",
			"results": test_result,
			"inputstatus": input_status.order_by('-id')[0],
			"arduinostatus":arduino_status.order_by('-id')[0],
			"avaliable":"yes"
		}
	else:
		context = {
			"user": user,
			"tag": "result",
			"results": test_result,
			"avaliable":"no"
		}
	return render(request, "result.html", context)

def test(request):
	if request.method == "POST":
		context = {
			"board": request.POST["arduino_board_no"],
			"bloodpressure": request.POST['bloodpressure'],
			"glucose": request.POST['glucose']
		}
		return render(request, "test.html", context)

	return HttpResponse("Nothing posted.")















