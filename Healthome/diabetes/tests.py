# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import Client

from django.urls import reverse

from .models import *
from . import views

class DiabetesRegisterTest(TestCase):
	def test_create_user(self):
		user = User.objects.create_user(
				username = "unittest@email.com",
				password = "password",
				email = "unittest@email.com",
				first_name = "firstname",
				last_name = "lastname"
			)
		user.save()

	def test_register_view(self):
		response = self.client.get("/register/", follow=True)
		self.assertEqual(response.resolver_match.func, views.register)

	def test_register_new_user(self):
		data = {
			"email": "unittest@email.com",
			"password": "password",
			"firstname": "firstname",
			"lastname": "lastname"
		}
		response = self.client.post('/register/', data=data, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertRedirects(response,'/diabetes/')


class DiabetesLoginTest(TestCase):
	def setUp(self):
		user = User.objects.create_user(
				username = "test@test.com",
				password = "123456",
				email = "test@test.com",
				first_name = "firstname",
				last_name = "lastname"
			)
		user.save()

	def test_index(self):
		response = self.client.get('/diabetes/', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Email")
		self.assertContains(response, "Password")
		self.assertEqual(response.resolver_match.func, views.index)

	def test_login_valid(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		response = self.client.post('/diabetes/', data=data, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func, views.profile)
		self.assertRedirects(response,'/diabetes/profile/')

	def test_login_invalid(self):
		data = {
			"email": "test@test.com",
			"password": "nopassword"
		}
		response = self.client.post('/diabetes/', data=data, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "The email and password pair does not exist.")
		self.assertEqual(response.resolver_match.func, views.index)


class DiabetesProfileTest(TestCase):
	def setUp(self):
		user = User.objects.create_user(
				username = "test@test.com",
				password = "123456",
				email = "test@test.com",
				first_name = "firstname",
				last_name = "lastname"
			)
		user.save()
		board = ArduinoBoard(
					user=user,
					board="123456",
					used='True'
				)
		board.save()

	def test_profile_view(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		self.client.post('/diabetes/', data=data, follow=True)
		response = self.client.get('/diabetes/profile/', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func, views.profile)
		self.assertContains(response, "firstname")
		self.assertContains(response, "lastname")

	def test_profile_add_new_board(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		self.client.post('/diabetes/', data=data, follow=True)
		board_data = {
			"add": "add",
			"add_board": "1234567890"
		}
		response = self.client.post('/diabetes/profile/', data=board_data, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func, views.profile)
		self.assertContains(response, "1234567890")

	def test_profile_delete_board(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		self.client.post('/diabetes/', data=data, follow=True)
		board_data = {
			"delete": "delete",
			"delete_board": "123456"
		}
		response = self.client.post('/diabetes/profile/', data=board_data, follow=True)
		self.assertRedirects(response,'/diabetes/profile/')
		self.assertNotContains(response, "123456")


class DiabetesInputTest(TestCase):
	def setUp(self):
		user = User.objects.create_user(
				username = "test@test.com",
				password = "123456",
				email = "test@test.com",
				first_name = "firstname",
				last_name = "lastname"
			)
		user.save()
		board = ArduinoBoard(
					user=user,
					board="123456",
					used='True'
				)
		board.save()
		inputstatus = InputBodyStatus(
				user=user,
				pregnant="1",
				skinfold="20",
				seruminsulin="20",
				bmi="20",
				pedigree="0.5",
				age="20"
			)
		inputstatus.save()

	def test_input_view(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		self.client.post('/diabetes/', data=data, follow=True)
		response = self.client.get('/diabetes/input/', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func, views.input)
		self.assertContains(response, "20")
		self.assertContains(response, "0.5")
		self.assertContains(response, "input")

	def test_input_new(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		self.client.post('/diabetes/', data=data, follow=True)
		input_data = {
			"pregnant": "1",
			"skinfold": "201",
			"seruminsulin": "201",
			"bmi": "201",
			"pedigree": "0.52",
			"age": "201"
		}
		response = self.client.post('/diabetes/input/', data=input_data, follow=True)
		self.assertContains(response, "201")
		self.assertContains(response, "Body status saved successfully!")


class DiabetesArduinoTest(TestCase):
	def setUp(self):
		user = User.objects.create_user(
				username = "test@test.com",
				password = "123456",
				email = "test@test.com",
				first_name = "firstname",
				last_name = "lastname"
			)
		user.save()
		board = ArduinoBoard(
					user=user,
					board="123456",
					used='True'
				)
		board.save()
		arduino_status = TestBodyStatus(
				user=user,
				glucose="20",
				bloodpressure="70"
			)

	def test_arduino_view(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		self.client.post('/diabetes/', data=data, follow=True)
		response = self.client.get('/diabetes/arduino/', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func, views.arduino)
		self.assertContains(response, "20")
		self.assertContains(response, "arduino")

	def test_arduino_create_with_get(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		self.client.post('/diabetes/', data=data, follow=True)
		response = self.client.get('/diabetes/arduino/?arduino_board_no=123456&glucose=70', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Save successfully!")
		response = self.client.get('/diabetes/arduino/?arduino_board_no=123456&bloodpressure=70', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Save successfully!")

	def test_arduino_create_with_post(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		self.client.post('/diabetes/', data=data, follow=True)
		arduino_data = {
			"glucose": "80",
			"bloodpressure": "80"
		}
		response = self.client.post('/diabetes/arduino/', data=arduino_data, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Arduino Board test result got successfully!")


class DiabetesResultTest(TestCase):
	def setUp(self):
		user = User.objects.create_user(
				username = "test@test.com",
				password = "123456",
				email = "test@test.com",
				first_name = "firstname",
				last_name = "lastname"
			)
		user.save()
		board = ArduinoBoard(
					user=user,
					board="123456",
					used='True'
				)
		board.save()
		arduino_status = TestBodyStatus(
				user=user,
				glucose="20",
				bloodpressure="70"
			)
		arduino_status.save()
		inputstatus = InputBodyStatus(
				user=user,
				pregnant="1",
				skinfold="20",
				seruminsulin="20",
				bmi="20",
				pedigree="0.5",
				age="20"
			)
		inputstatus.save()

	def test_result_view(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		self.client.post('/diabetes/', data=data, follow=True)
		response = self.client.get('/diabetes/result/', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, "%")

	def test_result_add(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		self.client.post('/diabetes/', data=data, follow=True)
		result_data = {
			"add": "add"
		}
		response = self.client.post('/diabetes/result/', data=result_data, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "%")

	def test_result_delete(self):
		data = {
			"email": "test@test.com",
			"password": "123456"
		}
		self.client.post('/diabetes/', data=data, follow=True)
		result_data = {
			"add": "add"
		}
		response = self.client.post('/diabetes/result/', data=result_data, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "%")
		result_data = {
			"delete": "delete",
			"recordID": 1
		}
		response = self.client.post('/diabetes/result/', data=result_data, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, "%")


class DiabetesTestTest(TestCase):

	def test_test_view(self):
		response = self.client.get('/diabetes/test/', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Nothing posted.")

# Create your tests here.
