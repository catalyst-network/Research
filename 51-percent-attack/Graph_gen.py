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



########################################
# plot_ratio_VMinOverV_vsN: Distribution of minimum ratio Vmin/V for probability <= thre as a function of N (probability increase with Vmin/V)
# params:
# rO: fraction  O/N
# rangeN: range of N values
# thre: threshold probability of attack
# lowV: minimum value for V
# rV: fraction V/N

def plot_ratio_VMinOverV_vsN(rO,rV,rangeN,thre,lowV):
        pH=[]
        rN=[]
        for Ni in rangeN: 
            # Find the lowest N for which the function applies given lowV
            lowN = int(math.floor(lowV/rV))
            #print("lowN, N --> ", lowN, ", ", Ni)
            if Ni < lowN:
                continue
            O = int(math.floor(Ni*rO)) 
            V = int(math.floor(Ni*rV))
            Vmin_tmp = math.floor(0.001*V)
            Vmin = max(Vmin_tmp,lowV)
                
            #print("N, O, V: ",Ni,", ",O,", ",V," varying Vmin to find proba < ",thre)
            
            proba_thre = 1
            Vi = Vmin
            Vbin = 5
            Vthre = 0
            while proba_thre > thre:
                p = math.floor(Vi/2) 
                proba_thre = hypergeom.sf(p, Ni, O, Vi)
                
                Vthre = Vi
                #print(Vi,", prob --> ",proba_thre)
                Vi = Vi + Vbin
            #print("--> ",float(Vthre)/float(V))
            
            pH.append(float(Vthre)/float(V))
            rN.append(Ni)
            
        return (rN, pH)


########################################
# plot_ratio_VOverN: Distribution of minimum ratio V/N for probability <= thre as a function of N (probability increase with V/N)
# params:
# rO: fraction  O/N
# rN: range of N values
# thre: threshold probability of attack
# lowV: minimum value for V
# 
# Output:
# rangeN: Value for Ni (assuming it have a V value > than lowV) 
# pH: The ratio between the V value where the threshold was reached and the relevant N value

def plot_ratio_VoverN(rO,rN,thre,lowV):
        
        pH=[]
        rangeN=[]
        for Ni in rN: #For each rangeN in range 5k - 100k
            Vmin = max(0.001*Ni,lowV) #Minumum value of V is 0.001 of the value of the range interval 
            #Vmin = math.max(V_min as defined in the parameters of the fonction 2000, math.floor(0.001*Ni)
            #print("lowN, N --> ", Vmin, ", ", Ni)
            if Ni < lowV:
                print("check your param")
                continue   
            O=Ni*rO #O = Each range x the ratio of bad nodes specified 
            #print("N, O: ",Ni,", ",O,". Varying V to find proba ~ 10-9")
            
            proba_thre = 1 
            Vi = Vmin #rVi is set to 0.001 of the value of the range interval 
            Vbin = 5 #bin size of 10 
            V_thre = 0 

            while proba_thre > thre: #while value set on l32 > value set on l52 ...
                p = math.floor(Vi/2) + 1 #math.floor rounds to the nearest value 
                proba_thre = hypergeom.sf(p, Ni, O, Vi)
                V_thre = Vi
                #print(Vi,", prob --> ",proba_thre)
                Vi = Vi + Vbin

            if V_thre < lowV:
                print("failed for (N,V,O) = (",Ni,", ",V_thre,", ",rO*100,") --> ",float(V_thre)/float(Ni))
                continue
            #else:
                #print("success for (N,V,O) = (",Ni,", ",V_thre,", ",rO*100,") --> ",float(V_thre)/float(Ni))
            pH.append(float(V_thre)/float(Ni))
            rangeN.append(Ni)        
                   
        return (rangeN,pH)


########################################
# plot_ratio_VMinOverV_vsN: Distribution of minimum ratio Vmin/V for probability <= thre as a function of N (probability increase with Vmin/V)
# params:
# rO: fraction  O/N
# rN: range of N values
# thre: threshold probability of attack
# lowV: minimum value for V
# 
# Output:
# rangeN: Value for Ni (assuming it have a V value > than lowV) 
# pH: The ratio between the V value where the threshold was reached and the relevant N value


def plot_ratio_VMinOverV(rO,rN,thre):
        pH=[]
        for rNi in rN: #Will stay the same as we want x axis to be over N
            O=rNi*rO #Will stay the same as we want to show vairying mallicious nodes
            #print("N, O: ",rNi,", ",O,". Varying V to find proba ~ $10^-9$") #Stays the same
            V = rNi*0.2 #Set the V to N ratio
            Vmin = math.floor(0.001*V)
            proba_thre = 1
            rVi = Vmin
            Vbin = 5
            VMin_thre = 0
            while proba_thre > thre:
                p = math.floor(rVi/2) 
                proba_thre = hypergeom.sf(p, rNi, O, rVi)
                VMin_thre = rVi
                #print(rVi,", prob --> ",proba_thre)
                rVi = rVi + Vbin
            #print("--> ",V_thre/N)
            pH.append(VMin_thre/V) #Needs to be VMin_thre / V
        return (pH)


def plot_thresholdO_over_N(rN, rVoN, threshold):
    #rVoN: a ratio
    #rN: range of N values
    curveOoN=[]
    for irN in rN:
        V = math.floor(irN * rVoN)
        binO = 0.001
        itO = 0.001
        max_fracO = 0
        proba = 0
        while proba < threshold:
            p = math.floor(V/2) + 1
            O = math.floor(itO*irN)
            proba = hypergeom.sf(p,irN,O, V)
            max_fracO = itO
            itO = itO + binO    
        curveOoN.append(max_fracO)
    return curveOoN

def plot_cummulative_over_rangeO(rR,N,V):
        
        pH=[]
        pB=[]
        p = math.floor(V/2) + 1
        #print("N, V: ",N,", ",V,". Varying O:")
        for rRi in rR:
            O=N*rRi
            pH.append(hypergeom.sf(p, N, O, V))
            #print(O," --> ", hypergeom.sf(p, N, O, V))
            pB.append(binom.sf(p,V,rRi))
        return (pH,pB)


def plot_multiple_cummulative_over_rangeO(rR,N,V):
        
        pH=[]
        pB=[]
        p = math.floor(V*0.5) + 1
        #print("N, V: ",N,", ",V,". Varying O:")
        for rRi in rR:
            O=N*rRi*0.01
            pH.append(hypergeom.sf(p, N, O, V))
            #print(V,", ",O," --> ", hypergeom.pmf(p, N, O, V))
        return (pH)

def plot_cummulative_over_rangeV(rO,N,rV):
        pH=[]
        pB=[]
        O=N*rO
        #print("N, O: ",N,", ",O,". Varying V:")
        for rVi in rV:
            p = math.floor(rVi/2) + 1
            pH.append(100*hypergeom.sf(p, N, O, rVi))
            #print(O," --> ", hypergeom.sf(p, N, O, rVi))
            pB.append(100*binom.sf(p,rVi,rO))
        return (pH,pB)        

def plot_cummulative_over_rangeVmin(rO,N,rVmin):
        pH=[]
        pB=[]
        O=N*rO
    
        for rVi in rVmin:
            pmin = math.floor(rVi/2) + 1
            pH.append(hypergeom.sf(pmin, N, O, rVi))
            #print(O," --> ", hypergeom.sf(pmin, N, O, rVi))
            pB.append(binom.sf(pmin,rVi,rO))
        return (pH,pB)        
