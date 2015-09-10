import numpy as np
from matplotlib.pylab import *
import matplotlib.animation as animation
from mpl_toolkits.axes_grid1 import host_subplot
from datetime import datetime
from matplotlib.colors import cnames
import pdb
import matplotlib.dates as mdates
import va_read_data as parse
import csv


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

# We read in the data
#columns = parse.read_in('va_air_data.csv')

TimeAxis = []
n = 1480
nPerFrame = 24
for i in np.arange(0,n):
    TimeAxis.append(mdates.date2num(datetime.strptime(columns['Date'][i] + " " + columns['Time'][i],"%d.%m.%Y %H:%M")))
"""TO DO"""


# Set up the rc settings,
# Our fonts should be latex style
#matplotlib.rc('text', usetex=True)
#matplotlib.rc('font', family='serif')
font = {'size' :12}


# Setup figure and subplots
f0 = figure(num = 0, figsize = (12,8))#, dpi = 100)
f0.suptitle('Amount of PM10')

#Define the subplot/subplotgrid
ax01 = subplot(111)
#ax01 = subplot2grid((2,2),(0,0))

ax01.set_title('PM10')

ax01.set_ylim(-0.1,2.0)

ax01.set_xlim(TimeAxis[0],TimeAxis[nPerFrame])

ax01.set_xlabel('Time of Day')

ax01.set_ylabel('Ratio between aquired data and dangerous limits')

""" Let's make one line for each day of the week, each line with a different color"""
colors = plt.cm.jet(np.linspace(0,1,7))

lines = []
time = []
pm10 = []
pm25 = []
no2 = []


ax01.set_xticks(TimeAxis[0:48])

ax01.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax01.axhline(y = 30.0/75.0,color='r',label = 'Yearly average limit of NO2 levels')

Plot_pm10, = ax01.plot_date(time, pm10, '-')
Plot_no2, = ax01.plot_date(time, no2, '-',color='#b58900',lw = 3)
Plot_pm25, = ax01.plot_date(time, pm25, '-')


# Format the x-axis for dates (label formatting, rotation)
f0.autofmt_xdate(rotation=45)
f0.tight_layout()
backgrCol = '#5D5FA4' 
xmax = 48
x = 0 
maxRad = float(max(columns['Rad'][1:n]))
# animation function, this is called sequentially
def updateData(self):
    global x
    global time
    global pm10
    global alpha
#I#    time.append(datetime.strptime(columns['Time'][x],"%H:%M"))
    time.append(TimeAxis[x])
    
    if x >= xmax:
        no2.pop(0)
        no2.append(float(columns['NO'][x])*(1.0/75.0))

    no2.append(float(columns['NO'][x])*(1.0/75.0))
    # pm25.append(float(columns['Dust2.5'][x])*(1.0/50.0))
    # pm10.append(float(columns['Dust10'][x])*(1.0/50.0))
    x = x + 1
    radiation = 1.0 - float(columns['Rad'][x])*(1.0/maxRad) 
    ax01.axvspan(TimeAxis[x],TimeAxis[x+1],facecolor=backgrCol,alpha=radiation,lw = 0)
    
    ax01.legend([Plot_no2],[columns['Date'][x]])
    # Plot_pm10.set_data(time,pm10)
    Plot_no2.set_data(time,no2)
    # Plot_pm25.set_data(time,pm25)
    if x >= xmax-1:
        ax01.set_xlim(TimeAxis[x-xmax],TimeAxis[x+1])
        ax01.set_xticks(TimeAxis[x-xmax:x+1])
        # now we don't need these values any more.
    return Plot_no2 #, Plot_pm25, Plot_pm10

anim = animation.FuncAnimation(f0, updateData, frames=n, interval=10, blit=False, repeat=False)

#I# anim.save('va_animation.mp4', fps=1, extra_args=['-vcodec','libx264'])

plt.show()
