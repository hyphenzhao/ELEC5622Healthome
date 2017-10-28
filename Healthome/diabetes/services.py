import csv
import math
import os
from django.conf import settings
from decimal import Decimal

def calculate_probability(testPoint):

	yes = Decimal(1.0)
	yessize = Decimal(1.0)
	nosize = Decimal(1.0)
	no = Decimal(1.0)
	index = 0
	file_path = os.path.join(settings.BASE_DIR, 'static/data/pima_output.csv')
	with open(file_path, 'rb') as csvfile:
		pima = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in pima:
			if len(row) == 2:
				yes = Decimal(row[0])
				no = Decimal(row[1])
				yessize = Decimal(row[0])
				nosize = Decimal(row[1])
			elif len(row) == 4:
				data = Decimal(testPoint[index])
				if data <= Decimal(0):
					data = (Decimal(row[0]) * yessize + Decimal(row[2]) * nosize) / (yessize + nosize)
				yes *= single_probability(Decimal(row[0]), Decimal(row[1]), data)
				no *= single_probability(Decimal(row[2]), Decimal(row[3]), data)
				index += 1
	if (yes + no) == Decimal(0.0):
		return 0.0
	result = (yes * Decimal(100.0)) / (yes + no)

	return result

def single_probability(mean, sd, x):

	exponent = -Decimal(math.pow(x - mean, Decimal(2.0))) / (Decimal(2.0) * Decimal(math.pow(sd, Decimal(2.0))))
	index = Decimal(1.0) / (sd * Decimal(math.sqrt(Decimal(2.0) * Decimal(math.pi))))
	result = index * Decimal(math.exp(exponent))

	return result

# t = [6,148,72,35,155,33.6,0.627,50]
# print calculate_probability(t)