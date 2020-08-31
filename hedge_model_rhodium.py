#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 17:45:26 2020

@author: seanmurphy
"""

from rhodium import * #import rhodium must be first line

from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import matplotlib.pyplot as plt
import time

start = time.time()

# import constant inputs

# Hub prices
HubPrices = pd.read_csv('stoch_hub.csv',header=0,index_col=0)
HubPricesConst = HubPrices.loc[0:17519,:].values

# Node prices
NodePrices = pd.read_csv('stoch_nodal.csv',header=0,index_col=0)
NodePricesConst = NodePrices.loc[0:17519,:].values

# Wind power production
WindPower = pd.read_csv('stoch_wind.csv',header=0,index_col=0)
WindPowerConst = WindPower.loc[0:17519,:].values

# Calendar lookup
calendar = pd.read_csv('calendar.csv',header=0)
a = range(24)
b = np.tile(a,365)
calendar['Hours'] = b
years = int(len(HubPricesConst)/8760)
calendarConst = calendar.values

# strikeprice = 23
# hedgetargets = np.ones((12*2,1))*150
SP = 15.14


def simulate(hedgetargets, strikeprice = SP,
             HP = HubPricesConst,
             NP = NodePricesConst,
             WP = WindPowerConst,
             calendar=calendarConst):
    
    #set up empty vectors for values
    DeveloperProfits = 0
    DeveloperHedge = 0
    DeveloperRevs = 0
    TraderProfits = 0
    TraderRevs = 0
    DeveloperDaily = []
    
    for i in range(0,len(HP)):
        
        # what month, hour of the day is it?
        if i < 8760:
            j = i
        else:
            j = i%8760                    
        month = calendar[j,0]
        day_hour = calendar[j,2]
        
        # Profits
        
        if day_hour < 7 or day_hour > 22:
            p = 0
            
        else:  
            p = 1
        
        D = np.float(WP[i]*np.max([0,NP[i]]) - np.max([hedgetargets[(month-1)*2+p]-WP[i],0])*NP[i] + (strikeprice - HP[i])*hedgetargets[(month-1)*2+p])
        DeveloperDaily = np.append(DeveloperDaily,D)
        DeveloperProfits = DeveloperProfits + D
        DeveloperRevs = DeveloperRevs + np.max([0,D])
        T = np.float((HP[i] - strikeprice)*hedgetargets[(month-1)*2+p])
        TraderRevs = TraderRevs + np.max([0,T])
        TraderProfits = TraderProfits + T
        DeveloperHedge = DeveloperHedge + (strikeprice - HP[i])*hedgetargets[(month-1)*2+p]
        
          
    ratio = np.float(TraderRevs/DeveloperRevs)
    DeveloperHedge = np.float(DeveloperHedge)
                            
    return DeveloperProfits, ratio


# a,b = simulate(hedgetargets,strikeprice,HP=HubPricesConst,NP=NodePricesConst,WP=WindPowerConst,calendar=calendarConst)

# initialize model

model = Model(simulate) # simulate: function name

# parameters: all inputs, even constant ones, in double quotes

model.parameters = [Parameter("hedgetargets"),
                    Parameter("strikeprice"),
                    Parameter("HP"),
                    Parameter("NP"),
                    Parameter("WP"),
                    Parameter("calendar")]

# responses: outputs of interest
# using INFO records output but doesn't do anything with it

model.responses = [Response("DeveloperProfits", Response.MAXIMIZE),
                  Response("ratio", Response.MAXIMIZE)]

# constraints on outputs
    # not in the function yet, but i would recommend using this for:
        # generation meets hedge >= 90% of the time
    # given output of hedge goal satisfaction is "HedgeMet", format:

# model.constraints = [Constraint("np.hedgetargets[0] + hedgetargets[1] + hedgetargets[0] + hedgetargets[1] + hedgetargets[0] + hedgetargets[1] + hedgetargets[0] + hedgetargets[1]" 
model.constraints = [Constraint("7*(hedgetargets[0] + hedgetargets[2] + hedgetargets[4] + hedgetargets[6] + hedgetargets[8] + hedgetargets[10] + hedgetargets[12] + hedgetargets[14] + hedgetargets[16] + hedgetargets[18] + hedgetargets[20] + hedgetargets[22]) + 17*(hedgetargets[1] + hedgetargets[3] + hedgetargets[5] + hedgetargets[7] + hedgetargets[9] + hedgetargets[11] + hedgetargets[13] + hedgetargets[15] + hedgetargets[17] + hedgetargets[19] + hedgetargets[21] + hedgetargets[23])>= 10000")] #25470
                     # Constraint("7*hedgetargets[2] + 17*hedgetargets[3] >= 2049"),
                     # Constraint("7*hedgetargets[4] + 17*hedgetargets[5] >= 2240"),
                     # Constraint("7*hedgetargets[6] + 17*hedgetargets[7] >= 2709"),
                     # Constraint("7*hedgetargets[8] + 17*hedgetargets[9] >= 1977"),
                     # Constraint("7*hedgetargets[10] + 17*hedgetargets[11] >= 2185"),
                     # Constraint("7*hedgetargets[12] + 17*hedgetargets[13] >= 1835"),
                     # Constraint("7*hedgetargets[14] + 17*hedgetargets[15] >= 1522"),
                     # Constraint("7*hedgetargets[16] + 17*hedgetargets[17] >= 1976"),
                     # Constraint("7*hedgetargets[18] + 17*hedgetargets[19] >= 2238"),
                     # Constraint("7*hedgetargets[20] + 17*hedgetargets[21] >= 2653"),
                     # Constraint("7*hedgetargets[22] + 17*hedgetargets[23] >= 2054")] 

# levers   
model.levers = [RealLever("hedgetargets", 0, 250, length = 24)] # considering hedge target as 24 hour vectors each month
                # RealLever("strikeprice", 14, 26, length = 1)]

# run model

# nruns = 15000
# out = optimize(model, "NSGAII", nruns)

# # rhodium output data structures are a bit funky
#     # all saved as csv
#     # outputs are saved as numbers
#     # input vectors are saved as strings, like:
#         # "[1, 2, 3]"
#     # if you want to plot the vector policies, you'll need custom plotters that convert string to vector
    
# savepath = 'results.csv'
# out.save(savepath)

strikeprice = 15.14
df_H = pd.read_excel('P50.xlsx',sheet_name = 'hedge_targets',header=None)
hedgetargets = df_H.values
a,b = simulate(hedgetargets,strikeprice,HP=HubPricesConst,NP=NodePricesConst,WP=WindPowerConst,calendar=calendarConst)
 # plt.plot(out.DeveloperProfits, out.ratio)

# df7 = pd.read_csv(savepath)
# df7 = df7.sort_values(by = ['DeveloperProfits']).reset_index()

# plt.plot(df7.DeveloperProfits, df7.ratio, c='b')
# plt.plot(a,b,marker='o',markersize = 3, color='r')

# plt.xlabel('Developer Profits ($)')
# plt.ylabel('Ratio')

# stop = time.time()
# elapsed = (stop - start)/60
# mins = str(elapsed) + ' minutes'
# print(mins)


