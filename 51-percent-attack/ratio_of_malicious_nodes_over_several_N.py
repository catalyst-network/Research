from Graph_gen import plot_multiple_cummulative_over_rangeO
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



Nvalues = [2000,5000,10000,20000]
strRangeN = '-'.join(str(e) for e in Nvalues)
rR = [30,32,36,38,40,42,44,46,48,50]
top = rR[-1]
bottom = rR[0]
curves = []
for rN in Nvalues:
    VRatio = 0.2
    V = rN*VRatio
    curve = plot_multiple_cummulative_over_rangeO(rR,rN,V)
    curves.append(curve)
for ind_curve in range(0,len(Nvalues)):
    fN = Nvalues[ind_curve]
    plt.plot(rR,curves[ind_curve],label='{} N'.format(fN))
print("Generating graphs....")
plt.xlim(bottom,top)
plt.yscale('log')
plt.xlabel('Fraction of malicious nodes (O) in validation pool set N')
plt.ylabel('Probability 51% attack')
thre_1 = 10**-6
thre_2 = 10**-9
plt.hlines(thre_1, bottom, top, colors='k', linestyles='dashed', label='{} threshold'.format(thre_1))
plt.hlines(thre_2, bottom, top, colors='k', linestyles='-.', label='{} threshold'.format(thre_2))
plt.legend(loc='lower right',prop={'size': 9})
plt.grid()
plt.savefig('Graphs/ratio_of_malicious_nodes_over_several_N/graph_prob_vs_O_over_N_{}_V_is_{}_of_N_O_range_{}_{}.png'.format(strRangeN,VRatio,bottom,top))