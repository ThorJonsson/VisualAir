import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import datetime

# This function yields a list of the mean values at each mesurement interval
# for a given date range
def mean_rng(air_data, start,end, chemical):

    # Make a list that contains the half an hourly mesurement intervals
    rng0 = pd.date_range('00:30','23:30',freq = 'H')
    rng1 = pd.date_range('00:00','23:00',freq = 'H')
    TimeRange = rng1.union(rng0)

    # This list will contain the half an hourly mesurement intervals as strings
    TimeStr = []
    # This list will contain the different date ranges according to the items in TimeStr
    DateRanges = []
    # This list will contain the data for the given chemical for all the items in DateRanges
    # The mean value of each list in DateRanges_data
    DateRange_mean = []

    for i in np.arange(0,48):
        # strings of mesurement times
        TimeStr.append(TimeRange[i].strftime('%H:%M'))
        # date range for a given mesurement time
        DateRanges.append(pd.date_range(start + ' ' +  TimeStr[i]
            ,end + ' ' + TimeStr[i], freq = '24H'))
        # makes lists of the data during the Date ranges
        DateRanges_data = pd.Series(air_data[chemical], index = DateRanges[i])
        DateRange_mean.append(DateRanges_data.mean())
    
    return DateRange_mean
    

if __name__ == "__main__":

	filename = 'air_data.csv'
        dateparse = lambda x: pd.datetime.strptime(x, '%d.%m.%Y %H:%M')
	air_data = pd.read_csv(filename, sep='\t', parse_dates=[['Date', 'Time']], date_parser = dateparse, index_col=['Date_Time'], comment='#')
        mean_rng(air_data, '2014-09-30', '2014-10-03', 'NO2')
