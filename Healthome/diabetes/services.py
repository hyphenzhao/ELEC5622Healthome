import csv
import math
import os
from django.conf import settings

def calculate_probability(testPoint):

	yes = 1.0
	yessize = 1.0
	nosize = 1.0
	no = 1.0
	index = 0
	file_path = os.path.join(settings.BASE_DIR, 'static/data/pima_output.csv')
	with open(file_path, 'rb') as csvfile:
		pima = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in pima:
			if len(row) == 2:
				yes = float(row[0])
				no = float(row[1])
				yessize = float(row[0])
				nosize = float(row[1])
			elif len(row) == 4:
				data = float(testPoint[index])
				if data == -1.0:
					data = (float(row[0]) * yessize + float(row[2]) * nosize) / (yessize + nosize)
				yes *= single_probability(float(row[0]), float(row[1]), data)
				no *= single_probability(float(row[2]), float(row[3]), data)
				index += 1
	result = (yes * 100.0) / (yes + no)

	return result

def single_probability(mean, sd, x):

	exponent = -math.pow(x - mean, 2.0) / (2.0 * math.pow(sd, 2.0))
	index = 1.0 / (sd * math.sqrt(2.0 * math.pi))
	result = index * math.exp(exponent)

	return result

# t = [6,148,72,35,155,33.6,0.627,50]
# print calculate_probability(t)