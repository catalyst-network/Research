from Graph_gen import plot_cummulative_over_rangeVmin
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

#This generates a graph demostrating the minimum number (Vmin) of nodes that report the correct delta needed to generate acceptable security levels. 




N = 20000
V_ratio = 0.2
V = N*V_ratio
rR1 = 0.4
Vmin=100
bin_Size = 5
rVmin = range(Vmin, int(V+bin_Size), bin_Size)
top = rVmin[-1] 
bottom = rVmin[0]
O = math.floor(rR1*N)
p1_Vmin = ""
textstr = '\n'.join((
    r'N = %.d' % (N, ),
    r'O = %.d' % (O, ),
    r'V = %.d' % (V, ),))
y_text = 1000000*rR1
#Plot for {Vmin}
print("Generating graphs....")
(p1_Vm,p2_Vm) = plot_cummulative_over_rangeVmin(rR1,N,rVmin)
plt.plot(rVmin, p1_Vm, label='hypergeometric dist')
plt.plot(rVmin, p2_Vm, label = 'binomial approx.')
plt.yscale('log')
plt.xlabel('Vmin (Number of validator nodes from validation pool that succesfully generate a delta)')
plt.xlim(0,top)
plt.ylabel('Probability 51% attack')
thre_1 = 10**-6
thre_2 = 10**-9
plt.hlines(thre_1, 0, V, colors='k', linestyles='-.', label='{}%'.format(thre_1))
plt.hlines(thre_2, 0, V, colors='k', linestyles='dashed', label='{}%'.format(thre_2))
plt.legend(loc='lower left')
plt.grid()
plt.text(Vmin,y_text, textstr, fontsize=10, position=(150, 6.737358984570953e-31),  bbox=dict(facecolor='none', edgecolor='black'))
plt.savefig('Graphs/VMin_of_V/graph_prob_vs_VMin_range_{}_to {}_N_{}_Vratio_{}_O_ratio_{}.png'.format(bottom,top,N,V_ratio,rR1))