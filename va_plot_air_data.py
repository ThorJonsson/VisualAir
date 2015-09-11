#!/bin/python
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime

with open('va_air_data.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter = '\t', quotechar = '|')

	comment = reader.next()
	headers = reader.next()

	columns = {}
	for header in headers:
		columns[header] = []
	
	for row in reader:
		for header, value in zip(headers, row):
			columns[header].append(value)
X = []
for i in range(0,48):
    X.append(datetime.datetime.strptime(columns['Time'][i],"%H:%M"))

Y = columns['NO'][0:48]

line, = plt.plot_date(X, Y)

plt.show()
