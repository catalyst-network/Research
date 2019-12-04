from scipy.stats import hypergeom
from scipy.stats import binom
from decimal import *
import numpy as np
import os
import math
from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import FormatStrFormatter
import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 0.1
mpl.rcParams['hatch.linewidth'] = 0.1

V = 2000
V2 = 200
r = 0.6 #Repeat for 0.7 and0.8
lowbin = 0
maxbin = 2
#x = np.arange(lowbin, maxbin+lowbin, 1)
x = np.linspace(0,1,2)
y = np.empty(len(x))
y.fill(r)
d = 4.42 * math.sqrt(r*(1-r)/V)
d2 = 4.42 * math.sqrt(r*(1-r)/V2)
print(d)
error = np.empty(len(x))
error.fill(d)
errorb = np.empty(len(x))
errorb.fill(d2)


x2 = np.linspace(1,2,2)
y2 = np.empty(len(x2))
y2.fill(1-r)
#y[1]=1-r
error2 = np.empty(len(x2))
error2.fill(d)
errorb2 = np.empty(len(x2))
errorb2.fill(d2)


tickbin = 1  
plt.xticks(np.arange(0,3,step=1))
plt.ylim(0,1)
plt.xlim(lowbin,maxbin)
plt.xlabel('#[h($\delta_L$)] bins',fontsize = 12)
plt.ylabel('r $\pm$ $\Delta r$',fontsize = 15)
# (99.999% confidence level)')
plt.axhline(y=.5)
#Second plot r +- delta_r
plt.plot(x, y, color='maroon',linestyle='--',label='_nolegend_')
plt.plot(x2, y2, color='maroon',linestyle='--',label='_nolegend_')
#Second plot 0.5 + delta_r
#plt.plot(x, y2, 'k-',color='forestgreen',linestyle=':',label='50% + $\Delta$ r')
plt.fill_between(x, y-errorb, y+errorb,edgecolor='black',linewidth=0.2, hatch='\\\\', facecolor='seashell', label='V={}'.format(V2))
plt.fill_between(x2, y2-errorb2, y2+errorb2,edgecolor='black',linewidth=0.2, hatch='\\\\', facecolor='seashell',label='_nolegend_')
plt.fill_between(x, y-error, y+error,edgecolor='black',linewidth=0.2, hatch='///', facecolor='azure', label='V={}'.format(V))
plt.fill_between(x2, y2-error2, y2+error2,edgecolor='black',linewidth=0.2, hatch='///', facecolor='azure',label='_nolegend_')
#props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
#plt.text(1.6,0.95,' r = ' + str(int(r*100)) + '% \n\n V = ' + str(V),verticalalignment='top',bbox=props)
plt.legend(title='r={}% \n $\Delta r(V)$ (99.999% CL):'.format(r), loc='upper right')
#plt.show()
plt.savefig('Graphs/histogram_r/bar_graph_rDeltaR_over_V_at_99.999_at_r_{}.png'.format(r))

