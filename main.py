import numpy as np
import matplotlib.pyplot as plt
import va_read_data
import va_simple_plot


if __name__ == "__main__":

	filename = 'air_data.csv'
	data = va_read_data.read_in(filename)
	Y = data['NO'][0:300]

	va_simple_plot.line_plot(Y)
