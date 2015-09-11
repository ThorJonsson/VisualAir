#!/bin/python
import csv
#import numpy as np
#import matplotlib.pyplot as plt


def read_in(filename):

	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter = '\t', quotechar = '|')
	
		data = reader.next()
		headers = reader.next()
	
		data = {}
		for header in headers:
			data[header] = []
		
		for row in reader:
			for header, value in zip(headers, row):
				data[header].append(value)

	
	return data

