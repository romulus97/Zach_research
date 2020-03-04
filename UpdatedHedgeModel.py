# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 17:12:32 2019

@author: jerothen
"""

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import matplotlib.pyplot as plt

#set up empty vectors for values
DeveloperHUBRevenue=[] #money the developer is paid by commodity trader
TraderRevenue=[] # money the commodities trader makes from wind developer making up difference between hub price and strike price
Strike=30# Hedge strike price variable, can be changed later 
DeveloperNodeRevenue=[] # money made from selling all energy produced into nodal market
DeveloperNodeCosts=[] # money lost from buying energy from nodal market to meet hedge target
DeveloperNoHedge = []

# Hub prices
HubPrices = pd.read_csv('stoch_hub.csv',header=0,index_col=0)
HubPrices = HubPrices.values

# Node prices
NodePrices = pd.read_csv('stoch_nodal.csv',header=0,index_col=0)
NodePrices = NodePrices.values

# Wind power production
WindPower = pd.read_csv('stoch_wind.csv',header=0,index_col=0)
WindPower = WindPower.values

# 8760 hours of hedge targets
HedgeTargets = pd.read_csv('hedge_targets_time_series.csv',header=0)
HT = HedgeTargets.values

Full_HedgeTargets = []

years = int(len(WindPower)/8760)

for i in range(0,years):
    Full_HedgeTargets = np.append(Full_HedgeTargets,HT)
    
# Create time series of hedge target/wind power differences
Full_HedgeTargets = np.reshape(Full_HedgeTargets,(len(Full_HedgeTargets),1))
Difference = WindPower - Full_HedgeTargets

#developer/ nodal market transactions

for i in range(0,len(HubPrices)):
    
    DeveloperNoHedge.append(WindPower[i,0]*np.max((0,NodePrices[i,0])))

    if Difference[i]>0: #if excess energy is generated, sell all energy to market at node price(includes excess energy and hedge target amount)
        DeveloperNodeRevenue.append(WindPower[i,0]*np.max((0,NodePrices[i,0])))
        DeveloperNodeCosts.append(0)
        
    elif Difference[i]<0:     #if not enough energy has been made, buy difference from market at node price to meet hedge target
        DeveloperNodeRevenue.append(WindPower[i,0]*np.max((0,NodePrices[i,0]))) #Still sell the energy that was made, even though target was not met
        DeveloperNodeCosts.append((Full_HedgeTargets[i]-WindPower[i])*NodePrices[i]) #money lost from buying energy

#Trader/ Developer transactions

for i in range(0,len(HubPrices)):
    
    if HubPrices[i,0]>Strike:
        TraderRevenue.append((HubPrices[i,0]-Strike)*Full_HedgeTargets[i]) #developer pays commodity trader
        DeveloperHUBRevenue.append(0)
    
    elif HubPrices[i,0]<Strike:
        DeveloperHUBRevenue.append((Strike-HubPrices[i,0])*Full_HedgeTargets[i]) #commodity pays developer
        TraderRevenue.append(0)


DNR=sum(DeveloperNodeRevenue)
DNC=sum(DeveloperNodeCosts)
DHR=sum(DeveloperHUBRevenue)
TR = sum(TraderRevenue)

print("Commodity Trader Revenue:$"), 
print(TR - DHR) #net gain for commodity trader, taking out money that was paid to developer        

print("Wind Developer Revenue:$"),
print(DNR + DHR - DNC - TR)

print("Commodity Trader Revenue/Developer HUB Revenue Ratio:"),
print((TR - DHR)/DHR)

# Preliminary analysis

# Compare developer revenues with and without hedge in place
WithHedge = np.array(DeveloperNodeRevenue) + np.array(DeveloperHUBRevenue) - np.array(DeveloperNodeCosts) - np.array(TraderRevenue)
NoHedge = np.array(DeveloperNoHedge)

# Convert to annual revenues
WithHedge_annual = []
NoHedge_annual = []

years = int(len(WithHedge)/8760)

for i in range(0,years):
    a = np.sum(WithHedge[i*8760:i*8760+8760])
    b = np.sum(NoHedge[i*8760:i*8760+8760])
    WithHedge_annual.append(a)
    NoHedge_annual.append(b)
    

plt.figure()
plt.plot(WithHedge_annual,'b')
plt.plot(NoHedge_annual,'r')
plt.ylim([0,1.5e7])

