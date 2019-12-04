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


N = 100000
Vvalues =[2000,20000,50000,60000,80000]
strRangeN = '-'.join(str(e) for e in Vvalues)
rR = [30,32,36,38,40,42,44,46,48,50]
top = rR[-1]
bottom = rR[0]
curves = []
for rV in Vvalues:
    curve = plot_multiple_cummulative_over_rangeO(rR,N,rV)
    curves.append(curve)
for ind_curve in range(0,len(Vvalues)):
    fN = Vvalues[ind_curve]
    plt.plot(rR,curves[ind_curve],label='{} V'.format(fN))
print("Generating graphs....")
plt.xlim(bottom,top)
#plt.ylim(0,1)
plt.yscale('log')
plt.xlabel('Fraction of malicious nodes (O) in validation pool set N')
plt.ylabel('Probability 51% attack')
thre_1 = 10**-6
thre_2 = 10**-9
plt.hlines(thre_1, bottom, top, colors='k', linestyles='dashed', label='{} threshold'.format(thre_1))
plt.hlines(thre_2, bottom, top, colors='k', linestyles='-.', label='{} threshold'.format(thre_2))
plt.legend(loc='lower left',prop={'size': 9})
plt.grid()
plt.savefig('Graphs/ratio_of_malicious_nodes_over_several_V/graph_prob_vs_O_over_N_{}_V_is_{}_of_N_O_range_{}_{}.png'.format(N,strRangeN,bottom,top))