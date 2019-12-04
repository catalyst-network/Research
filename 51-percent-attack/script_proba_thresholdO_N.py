from Graph_gen import plot_thresholdO_over_N
from scipy.stats import hypergeom
from scipy.stats import binom
from decimal import *
import numpy as np
import os
import math
from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib.axes as ax
import matplotlib.cm as cm
from matplotlib.ticker import FormatStrFormatter


  


#x-axis: N
#rangeN = [1000, 2000, 10000]
#rangeN = [2000, 5000]
NBin = 1000
rangeN = range(1000,10000+NBin,NBin)
#create stings for top and bottom of N range for labels
top = rangeN[-1] 
bottom = rangeN[0] 
#y-axis: fraction O/N
#curves: different ratio V/N
rangeVoN = [0.1,0.2,0.5]
#create string for VoN labels 
strRangeVoN = '-'.join(str(e) for e in rangeVoN)
#variables: probability threshold
prob_thre = 10**-9
curves = []
ind_curve = 0
curves = []
for irVoN in rangeVoN:
    curve = plot_thresholdO_over_N(rangeN, irVoN , prob_thre)
    #print(curve)
    curves.append(curve)
print(len(rangeVoN))
for ind_curve in range(0,len(rangeVoN)):    
    #print(ind_curve," --> ", curves[ind_curve])
    fVoN = math.floor(100*rangeVoN[ind_curve])
    plt.plot(rangeN,curves[ind_curve],label='{}%'.format(fVoN))
print(rangeN)
plt.grid()
plt.ylim(0,0.5) 
plt.xlim(0,top)
plt.yticks(np.arange(0, 0.55, step=0.05))   
plt.xlabel('N (total worker pool size)')
plt.ylabel('Max Ratio O/N for prob < {} for a succesful 51% attack'.format(prob_thre))
plt.legend(title='Ratio V/N',loc='lower right')
plt.savefig('Graphs/script_proba_thresholdO_N/O-over-N-range-{}-{}-for-V-over-N-{}-at-prob-{}.png'.format(bottom,top,strRangeVoN,prob_thre))