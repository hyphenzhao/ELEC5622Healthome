# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from django.urls import reverse

class DiabetesIndexViewTest(TestCase):
	def test_hello_world(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Hello, world. You're at the diabetes application index.")

# Create your tests here.
