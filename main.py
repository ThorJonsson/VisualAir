import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb

if __name__ == "__main__":

	filename = 'air_data.csv'
        dateparse = lambda x: pd.datetime.strptime(x, '%d.%m.%Y %H:%M')
	air_data = pd.read_csv(filename, sep='\t', parse_dates=[['Date', 'Time']], date_parser = dateparse, index_col=['Date_Time'], comment='#')
        pdb.set_trace()
        air_data['SO2'].plot()
	plt.show()


        # CO alltaf >0

	#exit()

	#va_simple_plot.line_plot(Y)

	#avgs, stdevs = va_avg_month_plot.get_monthly_avg(data)

	#print avgs['NO']
	#print stdevs['NO']

	#new_fig = va_avg_month_plot.bar_chart_plotter(data, 'NO')

	#plt.show()

