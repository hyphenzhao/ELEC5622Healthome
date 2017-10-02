# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class ArduinoBoard(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	board = models.CharField(max_length=30, unique=True)
	used = models.BooleanField(default=False)

class InputBodyStatus(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	pregnant = models.DecimalField(max_digits=25, decimal_places=15)
	skinfold = models.DecimalField(max_digits=25, decimal_places=15)
	seruminsulin = models.DecimalField(max_digits=25, decimal_places=15)
	bmi = models.DecimalField(max_digits=25, decimal_places=15)
	pedigree = models.DecimalField(max_digits=25, decimal_places=15)
	age = models.DecimalField(max_digits=25, decimal_places=15)
	inputdate = models.DateTimeField(auto_now_add=True, blank=True)

class TestBodyStatus(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	glucose = models.DecimalField(max_digits=25, decimal_places=15)
	bloodpresure = models.DecimalField(max_digits=25, decimal_places=15)
	testdate = models.DateTimeField(auto_now_add=True, blank=True)

# Create your models here.
