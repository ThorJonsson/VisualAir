import numpy as np
import matplotlib.pyplot as plt


to_float = lambda x: float(x)


def line_plot(X, Y):
	# X, Y numpy vectors of the same length


	line, = plt.plot(X, Y)
	plt.show()


def line_plot(Y):
	# plot with defaul x-values

	X = np.arange(0, len(Y))

	line, = plt.plot(X, map(to_float, Y))
	plt.show()
