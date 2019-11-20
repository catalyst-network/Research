from Graph_gen import *
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
plt.savefig('Graphs/graph_prob_vs_O_over_N_N{}_V{}_O_range_{}_{}.png'.format(N,V,bottom,top))

#################################################################################################################################

Nvalues = [2000,5000,10000,20000]
strRangeN = '-'.join(str(e) for e in Nvalues)
rR = [0.3,0.32,0.36,0.38,0.4,0.42,0.44,0.46,0.48,0.5]
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
plt.savefig('Graphs/graph_prob_vs_O_over_N_{}_V_is_{}_of_N_O_range_{}_{}.png'.format(strRangeN,VRatio,bottom,top))

#################################################################################################################################

N = 10000
VRatio = 0.2
V = int(N*VRatio)
rR1 = 0.4
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
plt.savefig('Graphs/graph_prob_vs_V_range{}-{}_N{}_O_{}.png'.format(bottom,top,V,N,O))


#################################################################################################################################

#x-axis: N
#rangeN = [1000, 2000, 10000]
#rangeN = [2000, 5000]
rangeN = range(20000,101000,1000)
#create stings for top and bottom of N range for labels
top = rangeN[-1] 
bottom = rangeN[0] 
#y-axis: fraction O/N
#curves: different ratio V/N
rangeVoN = [0.02,0.05,0.1,0.2,0.3]
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
plt.savefig('Graphs/O-over-N-range-{}-{}-for-V-over-N-{}-at-prob-{}.png'.format(bottom,top,strRangeVoN,prob_thre))


#################################################################################################################################

proba_thre = 10**-9
rangeN = range(5000,21000,1000) #Will stay the same as this determines the range of N
top = rangeN[-1] 
bottom = rangeN[0] 
Ovalues = [0.3,0.4,0.45]
#create string for VoN labels 
strRangeO = '-'.join(str(e) for e in Ovalues)
print("Generating graphs....")
curves = []
for rO in Ovalues:
    curve = plot_ratio_VoverN(rO,rangeN,proba_thre)
    curves.append(curve)
for ind_curve in range(0,len(Ovalues)):
    fO = math.floor(100*Ovalues[ind_curve])
    plt.plot(rangeN,curves[ind_curve],label='{}%'.format(fO))
top2 = top/10
plt.grid()
plt.ylim(0,0.5) #may have to be increased for higher thresholds
plt.yticks(np.arange(0, 0.55, step=0.05)) #may have to be increased for higher thresholds
plt.xticks(np.arange(bottom-top2, top+top2, step=top2))
plt.xlim(bottom,top)
plt.xlabel('N (total worker pool size)')
plt.ylabel('Ratio of V/N for prob < {}'.format(proba_thre))
plt.legend(title='Percentage O/N',loc='upper right')
plt.savefig('Graphs/graph_V_over_N_at_prob_{}vs_N_for_range_{}_to_{}_O_at_{}.png'.format(proba_thre,bottom,top,strRangeO))



#################################################################################################################################

proba_thre = 10**-9
rangeN = range(2000,11000,1000) #Will stay the same as this determines the range of N
top = rangeN[-1] 
bottom = rangeN[0] 
Ovalues = [0.3,0.4,0.45]
#create string for VoN labels 
strRangeO = '-'.join(str(e) for e in Ovalues)
print("Generating graphs....")
#rO=0.2
#p1VMinoN_1 = plot_ratio_VMinOverN(rO,rangeN,proba_thre)
curves = []
for rO in Ovalues:
    curve = plot_ratio_VMinOverN(rO,rangeN,proba_thre)
    curves.append(curve)

for ind_curve in range(0,len(Ovalues)):
    fO = math.floor(100*Ovalues[ind_curve])
    plt.plot(rangeN,curves[ind_curve],label='{}%'.format(fO))
top2 = top/10
plt.grid()
plt.ylim(0,1)
plt.yticks(np.arange(0, 1.05, step=0.10))
plt.xticks(np.arange(bottom-top2, top+top2, step=top2))
plt.xlim(bottom-1000,top+top2)
plt.xlabel('N (total worker pool size)')
plt.ylabel('Ratio of VMin/Min for prob < {}'.format(proba_thre))
plt.legend(title='Percentage O/N',loc='upper right')
plt.savefig('Graphs/graph_VMin_over_V_at_prob_{}vs_N_for_range_{}_to_{}_O_at_{}.png'.format(proba_thre,bottom,top,strRangeO))

#################################################################################################################################

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
plt.savefig('Graphs/graph_prob_vs_VMin_range_{}_to {}_N_{}_Vratio_{}_O_ratio_{}.png'.format(bottom,top,N,V_ratio,rR1))


#################################################################################################################################