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

r = 0.8 #Repeat for 0.7 and0.8
lowbin = 50
maxbin = 2000
x = np.arange(lowbin, maxbin+lowbin, 10)
y = np.empty(len(x)); 
y.fill(r)
d = y*(1-y)/x
# example error bar values that vary with x-position
#print(len(x))
#print(len(y))
error = np.empty(len(x))
y2 = np.empty(len(x))
ind_d = 0
V_match = 0
match_found = False

for i in range(len(d)):
    error[i] = 4.42 * math.sqrt(d[i])
    y2[i] = 0.5 + error[i]
    #print("V = ",x[i], " --> d = ",error[i])
    if y[i]-error[i] >= 0.5 and match_found == False:
        V_match = x[i]
        match_found = True
        print(V_match)
tickbin = int((round(maxbin,-3)-round(lowbin,-2))/10)    
plt.xticks(np.arange(round(lowbin,-2), round(maxbin,-3), tickbin))
plt.ylim(0.2,1)
plt.xlim(lowbin,maxbin)
plt.xlabel('V (producer nodes)',fontsize = 12)
plt.ylabel('r $\pm$ $\Delta r$',fontsize = 15)
# (99.999% confidence level)')
plt.axhline(y=.5)
#Second plot r +- delta_r
plt.plot(x, y, 'k-',color='maroon',linestyle='--',label='_nolegend_')
#Second plot 0.5 + delta_r
plt.plot(x, y2, 'k-',color='forestgreen',linestyle=':',label='50% + $\Delta$ r')
plt.fill_between(x, y-error, y+error,edgecolor='black',linewidth=0.2, hatch='///', facecolor='azure')
props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
plt.text(0.72*x[-1],0.43,' r = ' + str(int(r*100)) + '% \n\n min(V) = ' + str(V_match) + '\n\n at 99.999% CL',verticalalignment='top',bbox=props)
plt.legend(loc='lower center')

plt.savefig('Graphs/script_rdeltar/graph_rDeltaR_over_V_at_99.999_at_r_{}.png'.format(r))


