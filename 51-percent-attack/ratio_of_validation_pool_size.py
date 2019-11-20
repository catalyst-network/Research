from Graph_gen import plot_cummulative_over_rangeV
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
VRatio = 0.2
V = int(N*VRatio)
rR1 = 0.45
O = math.floor(rR1*N)
Vmin=500
binSize = 50
rV = range(Vmin,V+binSize,binSize)
top = rV[-1]
bottom = rV[0]
print("Generating graphs....")
#Plot for {V}
(p1_V,p2_V) = plot_cummulative_over_rangeV(rR1,N,rV)
plt.plot(rV,p1_V, label='hypergeometric dist')
plt.plot(rV, p2_V, label = 'binomial approx.')
plt.yscale('log')
plt.xlabel('V')
plt.xlim(bottom,top)
plt.ylabel('Probability 51% attack')
thre_1 = 10**-6
thre_2 = 10**-9
plt.hlines(thre_1, Vmin, V, colors='k', linestyles='dashed', label='{} threshold'.format(thre_1))
plt.hlines(thre_2, Vmin, V, colors='k', linestyles='-.', label='{} threshold'.format(thre_2))
plt.legend(loc='lower left')
plt.grid()
textstr = '\n'.join((
    r'N = %.d' % (N, ),
    r'O = %.d' % (O, ),))
y_text = 1000000*min(p1_V)
plt.text(Vmin,y_text, textstr, fontsize=10,bbox=dict(facecolor='none', edgecolor='black'))
plt.savefig('Graphs/ratio_of_validation_pool_size/graph_prob_vs_V_range{}-{}_N{}_O_{}.png'.format(bottom,top,N,O))