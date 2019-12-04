from Graph_gen import plot_ratio_VMinOverV_vsN
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

#N: total number of nodes in pool (validators)
#V: total number of working validators nodes (workers) 
#O: total number of malicious nodes in pool (malicious validators)
#p: total number of malicious nodes selected for validation (malicious workers)
#Vmin: mininim number of validating nodes (minimum hashes collected by a worker for a valid ratio r_i = m/V_i where V_min <= V_i <= V)


#This plot describes O at 20%, 30%, 40% and 45% of vairying N values and the minimum V/N value needed to obtain 10^-9 security



proba_thre = 10**-9
binN = 1000
rangeN = range(10000,20000+binN,binN) #Will stay the same as this determines the range of N
top = rangeN[-1]
bottom = rangeN[0] 
Ovalue = 0.45
lowV = 1000
rangeV = [100, 200, 500] #Has to be divided by 1000
topV = rangeN[-1]
bottomV = rangeN[0]
#create string for VoN labels 
#strRangeO = '-'.join(str(e) for e in Ovalue)
print ("Generating graphs ...")
curves = []
range_curves = []
for rV in rangeV:
    rV = float(rV)*0.001
    range_curve, curve = plot_ratio_VMinOverV_vsN(Ovalue,rV,rangeN,proba_thre,lowV)
    curves.append(curve)
    range_curves.append(range_curve)
    
for ind_curve in range(0,len(rangeV)):
    fO = 0.1*rangeV[ind_curve]
    plt.plot(range_curves[ind_curve],curves[ind_curve],label='{}%'.format(fO))
top2 = top/10
plt.grid()
plt.ylim(0,1) #may have to be increased for higher thresholds
plt.yticks(np.arange(0, 1, step=0.1)) #may have to be increased for higher thresholds


#if bottom < 3000:
#    plt.xticks(np.arange(3000, top+top2, step=top2))
#    plt.xlim(3000,top)
#    print('rangeN to low to give accuracte results, readjusting range')
#else:
stepX = (top-bottom)/10
plt.xticks(np.arange(bottom, top+stepX, step=stepX))
plt.xlim(bottom,top)

plt.xlabel('N (pool of workers)')
plt.ylabel('Ratio of V_min/V for prob < {}'.format(proba_thre))
plt.legend(title='Percentage V/N',loc='upper right')
plt.savefig('Graphs/Validation_pool_to_achieve_threshold2/graph_V_over_Vmin_at_prob_{}vs_N_for_range_{}_to_{}_and_V_at_range_{}_{}O_at_{}.png'.format(proba_thre,bottom,top,bottomV,topV,str(Ovalue)))

