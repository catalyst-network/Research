from Graph_gen import plot_ratio_VoverN
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

#\50, 100, 500, 1000, 2000

proba_thre = 10**-9
lowV = 500
binN = 1000
rangeN = range(50000,100000+binN,binN) #Will stay the same as this determines the range of N 0, 10000 and 10000 to 50000, 50000 to 100000
top = rangeN[-1] 
bottom = rangeN[0] 
Ovalues = [200,300,400,450]
#create string for VoN labels 
strRangeO = '-'.join(str(e) for e in Ovalues)
print("Generating graphs....")
curves = []
range_curves = []

max_y = 0

for rO in Ovalues:
    rO = float(rO)*0.0010
    range_curve, curve = plot_ratio_VoverN(rO,rangeN,proba_thre,lowV)
    max_y_temp = max(curve)
    if max_y_temp > max_y:
        max_y = max_y_temp
    curves.append(curve)
    range_curves.append(range_curve)
max_y_axis = round(max_y,1)
step_y_axis = max_y_axis * 0.1
#print("y max : ",max_y)
for ind_curve in range(0,len(Ovalues)):
    fO = 0.1*Ovalues[ind_curve]
    plt.plot(range_curves[ind_curve],curves[ind_curve],label='{}%'.format(fO))
#s=''
#textstr = '\n'.join((
#    r'lowV = %.d' % (lowV, ),))
#plt.text(lowV,s, textstr, fontsize=10, position=(7800, 0.33),  bbox=dict(facecolor='none', edgecolor='black'))
top2 = top/10
plt.grid()
plt.ylim(0,max_y_axis) #may have to be increased for higher thresholds
plt.yticks(np.arange(0, max_y_axis, step=step_y_axis)) #may have to be increased for higher thresholds
plt.xticks(np.arange(bottom-top2, top+top2, step=top2))
plt.xlim(bottom,top)
plt.xlabel('N (tpool of workers)')
plt.ylabel('min(V/N) for prob < {}'.format(proba_thre))
plt.legend(title=(r' V $\geq$ {} \n Percentage O/N:'.format(lowV)),loc='upper right')
plt.savefig('Graphs/Validation_pool_to_achieve_threshold/graph_V_over_N_at_prob_{}vs_N_for_range_{}_to_{}_O_at_{}_minV_at_{}.png'.format(proba_thre,bottom,top,strRangeO,lowV))

