# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:17:44 2020

@author: jkern
"""

import numpy as np
import pandas as pd
import no_hedge
import matplotlib.pyplot as plt

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import constant inputs
df_data = pd.read_csv('input_data.csv', header=0)
X = df_data.values
HubPrices = X[:,0]
NodePrices = X[:,1]
WindPower = X[:,2]

# Calendar lookup
calendar = pd.read_csv('calendar.csv',header=0)
a = range(24)
b = np.tile(a,365)
calendar['Hours'] = b
years = int(len(HubPrices)/8760)
calendar = calendar.values

strikeprice = 22.64

floor_months = 10

#####################################################################
##########              BASIS RISK SCENARIO        ########################
#####################################################################

# import matplotlib.pyplot as plt

BasisRisk = NodePrices - HubPrices
# plt.hist(BasisRisk,100)

bias = np.mean(BasisRisk)
spread = np.std(BasisRisk)

# Alter nodal prices
experiment = 'standard_normal'

if experiment == 'mean_zero':
    BasisRisk = BasisRisk - bias
elif experiment == 'mean_zero_10p_std':
    BasisRisk = (BasisRisk - bias)/(spread*(1-.10))
elif experiment == 'mean_zero_20p_std':
    BasisRisk = (BasisRisk - bias)/(spread*(1-.20))
elif experiment == 'mean_zero_30p_std':
    BasisRisk = (BasisRisk - bias)/(spread*(1-.30))    
elif experiment == 'mean_zero_40p_std':
    BasisRisk = (BasisRisk - bias)/(spread*(1-.40))    
elif experiment == 'mean_zero_50p_std':
    BasisRisk = (BasisRisk - bias)/(spread*(1-.50))
elif experiment == 'mean_zero_60p_std':
    BasisRisk = (BasisRisk - bias)/(spread*(1-.60))
elif experiment == 'mean_zero_70p_std':
    BasisRisk = (BasisRisk - bias)/(spread*(1-.70))
elif experiment == 'mean_zero_80p_std':
    BasisRisk = (BasisRisk - bias)/(spread*(1-.80))    
elif experiment == 'mean_zero_90p_std':
    BasisRisk = (BasisRisk - bias)/(spread*(1-.90))
elif experiment == 'mean_zero_10p_std':
    BasisRisk = (BasisRisk - bias)/(spread*(1-.10))
elif experiment == 'standard_normal':
    BasisRisk = (BasisRisk - bias)/(spread)
elif experiment == 'no_basis_risk':
    BasisRisk = 0
    
NodePrices = HubPrices + BasisRisk

# objective functions
filename = 'experiments/' + experiment + '/Objective_Functions.csv'
df_O = pd.read_csv(filename,header=0,index_col=0)
df_O.columns = ['Profits','F_change']
order = range(0,len(df_O))
df_O['order'] = order
S = df_O.sort_values('Profits')


#define (ranges from 0-99)
pick = 0 #0 = max floor improvement, 99 = max profits
row_to_explore = S.iloc[pick,2]

#####################################################################
##########         Performance Measures        ######################
#####################################################################

# Defined maximum (no hedge) revenues
N = no_hedge.sim(HubPrices,NodePrices,WindPower,calendar,floor_months)
max_rev = N[0]
sorted_monthly = np.sort(N[2])
floor = sum(sorted_monthly[0:floor_months])

#####################################################################


# hedgetargets
filename = 'experiments/' + experiment + '/Decision_Variables.csv'
df_H = pd.read_csv(filename,header=0,index_col = 0)

hedgetargets = df_H.iloc[row_to_explore,:].values
   
#set up empty vectors for values
DeveloperProfits = 0
DeveloperHedge = 0
DeveloperRevs = 0
DeveloperMonth = 0
TraderProfits = 0
TraderRevs = 0
DeveloperDaily = [],
Constraints = []
Monthly = [] 
month_hold = 1
MonthlyVar = 0 
mins = []

strikeprice = 22.64

HP = HubPrices
NP = NodePrices
WP = WindPower
RX = max_rev
V = floor
   
for i in range(0,len(HP)):
    
    # what month, hour of the day is it?
    if i < 8760:
        j = i
    else:
        j = i%8760                    
    month = calendar[j,0]
    day_hour = calendar[j,2]
    
    # Peak or off-peak hour     
    if day_hour < 6 or day_hour > 21:
        p = 0
        
    else:  
        p = 1
    
    # Financial exchange
    D = float(WP[i]*max([0,NP[i]]) - max([hedgetargets[(month-1)*2+p]-WP[i],0])*NP[i] + (strikeprice - HP[i])*hedgetargets[(month-1)*2+p])
    # DeveloperDaily = np.append(DeveloperDaily,D)
    DeveloperProfits += D
    
    T = float((HP[i] - strikeprice)*hedgetargets[(month-1)*2+p])
    TraderRevs += max([0,T])
    # TraderProfits += T
    
    DH = float((strikeprice - HP[i])*hedgetargets[(month-1)*2+p])
    DeveloperRevs += max([0,DH])
 
    # Monthly tracker
    if month != month_hold:
        month_hold = month
        Monthly.append(DeveloperMonth)
        
        if len(Monthly) <= floor_months:
            mins.append(DeveloperMonth)
        else:
            M = max(mins)
            if M > DeveloperMonth:
                idx = mins.index(M)
                mins[idx] = DeveloperMonth
        
        DeveloperMonth = D
                    
    else:
        DeveloperMonth += D

Ratio = float(TraderRevs/DeveloperRevs)
# DeveloperHedge = np.float(DeveloperHedge)
for i in range(0,len(Monthly)-1):
    MonthlyVar += abs(Monthly[i] - Monthly[i+1])
MonthlyVar = -MonthlyVar

VAR = sum(mins)
Floor_improvement = VAR - V
Profit_fraction = float(DeveloperProfits/RX)
results = [Profit_fraction, Floor_improvement]

print(results)
print(Monthly)

filename = 'Monthly' + str(row_to_explore) + '.txt'
np.savetxt(filename,Monthly)

plt.figure()
plt.plot(N[2])
plt.plot(Monthly)
plt.legend(['No Hedge','Hedge'])