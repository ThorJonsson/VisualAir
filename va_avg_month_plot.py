import numpy as np
import matplotlib.pyplot as plt


#def avg_month_bar_plot(data):


def get_monthly_avg(data):
	# create twelve vectors
	date_vector = data.pop('Date')
	time_vector = data.pop('Time')
	# data only contains the dependent variables

	data_monthly_avgs = {}
	data_monthly_stdevs = {}
	for variable in data:
		data_monthly_avgs[variable] = np.zeros(12)
		data_monthly_stdevs[variable] = np.zeros(12)
		# vectors containing average over jan, feb, etc


	for variable in data:
		# compute averages for this variable
		values_by_month = [[] for x in xrange(12)] # list containing 12 empty lists

		for index, date in enumerate(date_vector):

			value_string = data[variable][index]
			if not value_string.strip():
				# string is empty or only contains whitespace
				# do not add to average
				continue
			else:
				# string contains value
				try:
					value = float(value_string)
				except ValueError:
					# some read error occured, skip this entry
					print "Warning: value_string ", value_string , "not read"
					continue
				month = int(date[3:5]) - 1 # 1, 2, 3, etc.
				values_by_month[month].append(value)

		for month, list_of_vals in enumerate(values_by_month):
			data_monthly_avgs[variable][month] = np.mean(list_of_vals)
			data_monthly_stdevs[variable][month] = np.std(list_of_vals)


	return (data_monthly_avgs, data_monthly_stdevs)

def get_month_name(month_number):
	return {
			'1': 'january',
			'2': 'february',
			'3': 'march',
			'4': 'april',
			'5': 'may',
			'6': 'june',
			'7': 'july',
			'8': 'august',
			'9': 'september',
			'10': 'october',
			'11': 'november',
			'12': 'december'
			}[str(month_number)]
	

def autolabel(rects):
	max_height = 0
	for rect in rects:
		new_height = rect.get_height()
		max_height = max(max_height, new_height)
		
	for  rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x()+rect.get_width()/2.0, 
				0.5*max_height, '%d'%int(height),
				ha='center', va='bottom')

		return


def bar_chart_plotter(plot_data, variable_name):

	num_groups = 12 	# number of months
	avgs, stdevs = get_monthly_avg(plot_data)
	avg = avgs['NO']
	stdev = stdevs['NO']

	fig, ax = plt.subplots()
	index = np.arange(num_groups)
	bar_width = 0.35
	opacity = 0.4
	error_config = {'ecolor': '0.3'}

	rects = plt.bar(index, avg, bar_width,
			alpha=opacity,
			color='b',
			yerr=stdev,
			error_kw=error_config)
	autolabel(rects)

	plt.xlabel('Month')
	plt.ylabel('Average value')
	plt.title('Average ' + variable_name + ' by month')
	plt.xticks(index + 0.5*bar_width, 
			tuple(get_month_name(i) for i in range(1,13)))
	plt.tight_layout()

	return fig
