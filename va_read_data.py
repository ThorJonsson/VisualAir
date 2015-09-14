#!/bin/python
import csv
import numpy as np
import pandas as pd
from datetime import *
from dateutil.relativedelta import *
import calendar
import pdb

def read_in(filename):

	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter = '\t', quotechar = '|')
	
		headers = reader.next()
	
		data = {}
		for header in headers:
			data[header] = []
		
		for row in reader:
			for header, value in zip(headers, row):
				data[header].append(value)

	
	return data

# This function yields a list of the mean values at each mesurement interval
# for a given date range
def mean_rng(filename, start,final, chemical):
	dateparse = lambda x: pd.datetime.strptime(x, '%d.%m.%Y %H:%M')
	air_data = pd.read_csv(filename, sep='\t', parse_dates=[['Date', 'Time']], date_parser = dateparse, index_col=['Date_Time'], comment='#')
    	# Make a list that contains the half an hourly mesurement intervals
    	rng0 = pd.date_range('00:30','23:30',freq = 'H')
    	rng1 = pd.date_range('00:00','23:00',freq = 'H')
    	TimeRange = rng1.union(rng0)
	
	# Make a list of months
    	# This list will contain the data for the given chemical for all the items in DateRanges
    	# The mean value of each list in DateRanges_data
    	DateRange_mean = {}
	
	while start < final:
		end = start + relativedelta(months=+1) - relativedelta(days=+1)
    		# This list will contain the half an hourly mesurement intervals as strings
    		TimeStr = []
    		# This list will contain the different date ranges according to the items in TimeStr
    		Measure_range = []
		DateRange_mean.update({start.strftime('%B, %Y'): []})
    		for i in np.arange(0,48):
        		# strings of measurement times
        		TimeStr.append(TimeRange[i].strftime('%H:%M'))
       			# date range for a given measurement time
        		Measure_range.append(pd.date_range(start.strftime('%m-%d-%Y') + ' ' +  TimeStr[i],end.strftime('%m-%d-%Y') + ' ' + TimeStr[i], freq = '24H'))
        		# makes lists of the data during the Date ranges
        		DateRanges_data = pd.Series(air_data[chemical], index = Measure_range[i])
			DateRanges_data.tolist()
			DateRange_mean[start.strftime('%B, %Y')].append(DateRanges_data.mean())
    		start = start + relativedelta(months=+1)
    	return DateRange_mean
