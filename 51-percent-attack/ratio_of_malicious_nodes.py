from scipy.stats import hypergeom
from Graph_gen import plot_cummulative_over_rangeO
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



N = 10000
V = N*0.2
rR = [0.3,0.32,0.36,0.38,0.4,0.42,0.44,0.46,0.48,0.5]

#For labeling
top = rR[-1]
bottom = rR[0]

print("Generating graphs....")
#Plot for {O}
(p1_O,p2_O) = plot_cummulative_over_rangeO(rR,N,V)
plt.plot(rR,p1_O, label='hypergeometric dist.')
plt.plot(rR, p2_O, label = 'binomial approx.')
textstr = '\n'.join((
    r'N = %.d' % (N, ),
    r'V = %.d' % (V, ),))
plt.yscale('log')
plt.xlabel('Fraction of malicious nodes (O) in validation pool set N')
plt.xlim(bottom,top)
plt.ylabel('Probability 51% attack')
thre_1 = 10**-6
thre_2 = 10**-9
plt.hlines(thre_1, bottom, top, colors='k', linestyles='dashed', label='{} threshold'.format(thre_1))
plt.hlines(thre_2, bottom, top, colors='k', linestyles='-.', label='{} threshold'.format(thre_2))
y_text = ""
plt.text(N,V, textstr, fontsize=10, position=(0.465, 6.737358984570953e-72),  bbox=dict(facecolor='none', edgecolor='black'))
plt.legend(loc='lower right',prop={'size': 9})
plt.grid()
plt.savefig('Graphs/ratio_of_malicious_nodes/graph_prob_vs_O_over_N_N{}_V{}_O_range_{}_{}.png'.format(N,V,bottom,top))