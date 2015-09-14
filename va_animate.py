# Made by Thorsteinn Hjortur Jonsson 
# Date 13/09'15
# This tool uses matplotlib and pandas to make an animation using data on air quality
import numpy as np
from matplotlib.pylab import *
import matplotlib.animation as animation
from mpl_toolkits.axes_grid1 import host_subplot
from datetime import *
from matplotlib.colors import cnames
from dateutil.relativedelta import *
import calendar
import pdb
import matplotlib.dates as mdates
import va_read_data as parse

filename = 'air_data.csv'
# We read in the data
columns = parse.read_in(filename)
start = date(2014, 2, 1)
final = date(2015, 9, 1)
no2_data = parse.mean_rng(filename, start, final, 'NO2') 
rad_data = parse.mean_rng(filename, start, final, 'Radiation')
h2s_data = parse.mean_rng(filename, start, final, 'H2S')
pm10_data = parse.mean_rng(filename, start, final, 'Dust_PM10')
pm25_data = parse.mean_rng(filename, start, final, 'Dust_PM2.5')
# We have to make a list of all the times animated
TimeAxis = []
# Count number of steps
n = 0
for month in no2_data:
	n = n + len(no2_data[month])
# Number of hours in each figure
nPerFrame = 24
# To build the x axis
for i in np.arange(0,n):
    TimeAxis.append(mdates.date2num(datetime.strptime(columns['Date'][i] + " " + columns['Time'][i],"%d.%m.%Y %H:%M")))


#---------------------------------- Set up the rc settings,
font = {'size' :9}
matplotlib.rc('font', **font)
#---------------------------------- Setup figure and subplots
f0 = figure(num = 0, figsize = (12,8))#, dpi = 100)
f0.suptitle('Measurements of air in Reykjavik', fontsize=12)

#------------------------------Define the subplot/subplotgrid
ax01 = subplot2grid((2,2),(0,0), colspan=2, rowspan=1)
ax02 = subplot2grid((2,2),(1,0), colspan=2, rowspan=1)

#--------------------------------- Plot Settings
ax01.set_ylim(-0.1,3.5)
ax02.set_ylim(-0.1,5.0)

ax01.set_xlim(TimeAxis[0],TimeAxis[nPerFrame])
ax02.set_xlim(TimeAxis[0],TimeAxis[nPerFrame])

ax01.set_xlabel('Average Value at Time of Day During the Month')
ax02.set_xlabel('Average Value at Time of Day During the Month')

ax01.set_ylabel('Ratio between measured level and dangerous levels')
ax02.set_ylabel('Ratio between measured level and dangerous levels')

ax01.set_xticks(TimeAxis[0:nPerFrame])
ax02.set_xticks(TimeAxis[0:nPerFrame])

ax01.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax02.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

Plot_limit1 = ax01.axhline(y = 75.0/30.0,color='r',lw = 2,label = 'Recommended Limit of NO2 Levels')
Plot_limit2 = ax02.axhline(y = 50.0/20.0, color='r',lw = 2, label = 'Recommended Limit of PM10 Levels')
# These vectors will be the ones used for the animation
time = []
pm10 = []
pm25 = []
no2 = []
h2s = []

# Set the plots
Plot_pm10, = ax02.plot_date(time, pm10, '-',color='#b58900', lw = 2, label = 'PM10')
Plot_no2, = ax01.plot_date(time, no2, '-',color='#b58900',lw = 2, label = 'NO2')
Plot_pm25, = ax02.plot_date(time, pm25, '-', color='g',lw = 2, label = 'PM2.5' )
Plot_h2s, = ax01.plot_date(time, h2s, '-', color='g', lw = 2, label = 'H2S')

# Set legends
ax02.legend([Plot_pm10, Plot_pm25, Plot_limit2], [Plot_pm10.get_label(), Plot_pm25.get_label(), Plot_limit2.get_label()])
ax01.legend([Plot_no2, Plot_h2s, Plot_limit1], [Plot_no2.get_label(), Plot_h2s.get_label(), Plot_limit1.get_label()])

# Format the x-axis for dates (label formatting, rotation)
f0.autofmt_xdate(rotation=45)
f0.tight_layout()
backgrCol = '#073642' 
xmax = nPerFrame
x = 0
j = 0
month = date(2014,2,1)
maxRad = max(rad_data[month])
# animation function, this is called sequentially
def updateData(self):
    # We need to define global variables to run the loop through updateData
    global month
    global maxRad
    global x
    global j
    global time
    global pm10
    global alpha
    
    # We need to change months when we reach the end of the corresponding list
    if j == len(no2_data[month]):
        month = month + relativedelta(months=+1)
        j = 0
    # look at the maximum radiation for the month
        maxRad = max(rad_data[month])

    if x > xmax:
        # We can pop to save memory if x >= xmax we won't see those values any way
        time.pop(0)
        time.append(TimeAxis[x])
        no2.pop(0)
        no2.append(no2_data[month][j]*(1.0/30.0))
        pm10.pop(0)
        pm10.append(pm10_data[month][j]*(1.0/20.0))
        pm25.pop(0)
        pm25.append(pm25_data[month][j]*(1.0/20.0))
        h2s.pop(0)
        h2s.append(h2s_data[month][j]*(1.0/30.0))
        
        # Set the limits accordingly
        ax02.set_xlim(TimeAxis[x-xmax],TimeAxis[x+1])
        ax02.set_xticks(TimeAxis[x-xmax:x+1])
        
        ax01.set_xlim(TimeAxis[x-xmax],TimeAxis[x+1])
        ax01.set_xticks(TimeAxis[x-xmax:x+1])
        
        # The radiation function which is in charge of the background color
        radiation = np.abs(1.0 - rad_data[month][j]*1.0/maxRad) 
        ax01.axvspan(TimeAxis[x],TimeAxis[x+1],facecolor=backgrCol,alpha=radiation,lw = 0)
        ax02.axvspan(TimeAxis[x],TimeAxis[x+1],facecolor=backgrCol,alpha=radiation,lw = 0)
    else:
        # This is run at the beginning, we don't want to pop here
        time.append(TimeAxis[x])
        no2.append(no2_data[month][j]*(1.0/30.0))
        pm10.append(pm10_data[month][j]*(1.0/20.0))
        pm25.append(pm25_data[month][j]*(1.0/20.0))
        h2s.append(h2s_data[month][j]*(1.0/30.0))
        # To set the background color
        radiation = np.abs(1.0 - rad_data[month][j]*1.0/maxRad) 
        ax01.axvspan(TimeAxis[x],TimeAxis[x+1],facecolor=backgrCol,alpha=radiation,lw = 0)
        ax02.axvspan(TimeAxis[x],TimeAxis[x+1],facecolor=backgrCol,alpha=radiation,lw = 0)
    # The title is dynamic and tells the month 
    ax01.set_title(month.strftime('%B, %Y'))
    Plot_no2.set_data(time,no2)
    Plot_pm10.set_data(time,pm10)
    Plot_pm25.set_data(time,pm25)
    Plot_h2s.set_data(time, h2s)
    # x and j must be incremented equally so that the dimensions remain the same!
    x = x+1
    j = j+1
    return Plot_no2, Plot_h2s, Plot_pm25, Plot_pm10

anim = animation.FuncAnimation(f0, updateData, frames=n, interval=10, blit=False, repeat=False)

anim.save('va_animation.mp4', fps=2, extra_args=['-vcodec','libx264'])

plt.show()
