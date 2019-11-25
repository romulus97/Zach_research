# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 17:12:32 2019

@author: jerothen
"""

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np


#set up empty vectors for values
DeveloperHUBRevenue=[] #money the developer is paid by commodity trader
CommoditiesTraderRevenue=[] # money the commodities trader makes from wind developer making up difference between hub price and strike price
HedgePrice=21.36191 # Hedge strike price variable, can be changed later 
DeveloperNodeRevenue=[] # money made from selling all energy produced into nodal market
DeveloperNodeLosses=[] # money lost from buying energy from nodal market to meet hedge target


PriceList = pd.read_excel('LatestPricesandHedgeValues.xlsx', sheet_name='Sheet1')
#print(PriceList)

#Get all data into seperate lists
Difference= PriceList['Difference'] # Difference between amount of energy generated and hedge target 
RTHUB= PriceList['RT_hub']  #real time hub prices
RTNODE= PriceList['RT_node'] #real time node prices
Targets=PriceList['Target'] #Hedge Targets
WEnergy=PriceList['Energy'] #Amount of Energy produced


#developer/ nodal market transactions

for i in range(0,len(RTHUB)):
    if Difference[i]>0: #if excess energy is generated, sell all energy to market at node price(includes excess energy and hedge target amount)
        DeveloperNodeRevenue.append(WEnergy[i]*np.max((0,RTNODE[i])))
    elif Difference[i]<0:     #if not enough energy has been made, buy difference from market at node price to meet hedge target
        DeveloperNodeLosses.append((Targets[i]-WEnergy[i])*RTNODE[i]) #money lost from buying energy
        DeveloperNodeRevenue.append(WEnergy[i]*np.max((0,RTNODE[i]))) #Still sell the energy that was made, even though target was not met

#ComTrader/ Developer transactions

for i in range(0,len(RTHUB)):
    if RTHUB[i]>HedgePrice:
        CommoditiesTraderRevenue.append((RTHUB[i]-HedgePrice)*Targets[i]) #developer pays commodity trader
    elif RTHUB[i]<HedgePrice:
        DeveloperHUBRevenue.append((HedgePrice-RTHUB[i])*Targets[i]) #commodity pays developer
        


X=sum(DeveloperNodeRevenue)
Y=sum(DeveloperNodeLosses)
Z=sum(DeveloperHUBRevenue)

print("Commodity Trader Revenue:$"), 
print((sum(CommoditiesTraderRevenue))-Z) #net gain for commodity trader, taking out money that was paid to developer        

print("Wind Developer Revenue:$"),
print(X+Z-Y)

print("Commodity Trader Revenue/Developer HUB Revenue Ratio:"),
print(((float((sum(CommoditiesTraderRevenue)))-float(Z))/float(Z)))
