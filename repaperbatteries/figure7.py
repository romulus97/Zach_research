# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 21:03:50 2021

@author: jkern
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import no_hedge


#pick nodal colors -- keep consistent with figure 3
df = pd.read_csv('monthly_prices.csv',header=0)

L = list(df.columns)
L = L[2:12]

c = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan']
C = {}
for color in c:
    idx = c.index(color)
    C[L[idx]] = color
    
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(7.5,5.5))

#figure 7A

for node in L:
    df = pd.read_excel('ObservedBasisRisk_ObjectiveFunctionComparison.xlsx',sheet_name = node, header=None,index_col=0)
    
    ax1.plot(df.iloc[:,0],df.iloc[:,1]/1000,markeredgecolor=C[node],markersize=3,markerfacecolor='None',marker='o',linestyle='None')

ax1.set_xlabel('Fraction of Maximum Revenue',font='Arial',fontweight='bold')
ax1.set_ylabel('Floor Improvement ($1000s)',font='Arial',fontweight='bold')

plt.figlegend(L, loc = 'upper center', borderaxespad=0.1, ncol=3, labelspacing=0.34,  prop={'size': 7}, bbox_to_anchor=(0.432,1.0))  

#figure 7B

# Calendar lookup
calendar = pd.read_csv('../calendar.csv',header=0)
a = range(24)
b = np.tile(a,365)
calendar['Hours'] = b
# years = int(len(HubPrices)/8760)
calendar = calendar.values

strikeprice = 22.64

floor_months = 10

#####################################################################
##########              BASIS RISK SCENARIO        ########################
#####################################################################

# import matplotlib.pyplot as plt

# BasisRisk = NodePrices - HubPrices
# # plt.hist(BasisRisk,100)

# bias = np.mean(BasisRisk)
# spread = np.std(BasisRisk)


# if experiment == 'mean_zero':
#     BasisRisk = BasisRisk - bias
# elif experiment == 'mean_zero_10p_std':
#     BasisRisk = (BasisRisk - bias)/(spread*(1-.10))
# elif experiment == 'mean_zero_20p_std':
#     BasisRisk = (BasisRisk - bias)/(spread*(1-.20))
# elif experiment == 'mean_zero_30p_std':
#     BasisRisk = (BasisRisk - bias)/(spread*(1-.30))    
# elif experiment == 'mean_zero_40p_std':
#     BasisRisk = (BasisRisk - bias)/(spread*(1-.40))    
# elif experiment == 'mean_zero_50p_std':
#     BasisRisk = (BasisRisk - bias)/(spread*(1-.50))
# elif experiment == 'mean_zero_60p_std':
#     BasisRisk = (BasisRisk - bias)/(spread*(1-.60))
# elif experiment == 'mean_zero_70p_std':
#     BasisRisk = (BasisRisk - bias)/(spread*(1-.70))
# elif experiment == 'mean_zero_80p_std':
#     BasisRisk = (BasisRisk - bias)/(spread*(1-.80))    
# elif experiment == 'mean_zero_90p_std':
#     BasisRisk = (BasisRisk - bias)/(spread*(1-.90))
# elif experiment == 'standard_normal':
#     BasisRisk = (BasisRisk - bias)/(spread)
# elif experiment == 'no_basis_risk':
#     BasisRisk = 0
    
# NodePrices = HubPrices + BasisRisk

# Alter nodal prices
experiment = 'observed'
node = 'WFEC_MOORELAND_2'#'OKGEKEENANWIND' 'WFECVICILD2'

#define (ranges from 0-99)
pick = 0 #0 = max floor improvement, 99 = max profits

# objective functions
filename = '../experiments/' + node + '/' + experiment + '/Objective_Functions.csv'
df_O = pd.read_csv(filename,header=0,index_col=0)
df_O.columns = ['Profits','F_change']
order = range(0,len(df_O))
df_O['order'] = order
S = df_O.sort_values('Profits')

# import constant inputs
filename = '../experiments/' + node + '/' + experiment + '/input_data.csv'
df_data = pd.read_csv(filename, header=0)
X = df_data.values
HubPrices = X[:,0]
NodePrices = X[:,1]
WindPower = X[:,2]


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
filename = '../experiments/' + node + '/' + experiment + '/Decision_Variables.csv'
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
# print(Monthly)

filename = 'Monthly' + str(row_to_explore) + '.txt'
# np.savetxt(filename,Monthly)

# Compare to P99 Performance

# P99 hedgetargets
df_H = pd.read_excel('../P50.xlsx',sheet_name='hedge_targets',header=None)

hedgetargets = df_H.values
   
#set up empty vectors for values
DeveloperProfits = 0
DeveloperHedge = 0
DeveloperRevs = 0
DeveloperMonth = 0
TraderProfits = 0
TraderRevs = 0
DeveloperDaily = [],
Constraints = []
Monthly_P99 = [] 
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
        Monthly_P99.append(DeveloperMonth)
        
        if len(Monthly_P99) <= floor_months:
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
for i in range(0,len(Monthly_P99)-1):
    MonthlyVar += abs(Monthly_P99[i] - Monthly_P99[i+1])
MonthlyVar = -MonthlyVar

VAR = sum(mins)
Floor_improvement = VAR - V
Profit_fraction = float(DeveloperProfits/RX)
results = [Profit_fraction, Floor_improvement]

# print(results)
# print(Monthly_P99)

ax2.plot(np.array(N[2])/1000000,color='black',linewidth=1)
ax2.plot(np.array(Monthly)/1000000,color='deeppink',linewidth=1.2)
ax2.plot(np.array(Monthly_P99)/1000000,color='dodgerblue',linewidth=1.2,linestyle='--')
ax2.set_xticks([0,12,24,36,48])
ax2.set_xticklabels(['2015','2016','2017','2018','2019'])
ax2.set_xlabel('Year',fontname='Arial',fontweight='bold')
ax2.set_ylabel('Revenues ($ millions)',fontname='Arial',fontweight='bold')
ax2.legend(['No Hedge','Alternative','P99'],loc='upper right',borderaxespad=0.1, ncol=1, labelspacing=0.34,  prop={'size': 7}, bbox_to_anchor=(.94,.7))

plt.subplots_adjust(wspace=.25)

plt.savefig('figure7.png',dpi=800)