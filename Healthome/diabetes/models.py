# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class ArduinoBoard(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	board = models.CharField(max_length=30)
	used = models.BooleanField(default=False)
# Create your models here.
