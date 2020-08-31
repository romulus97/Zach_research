#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 17:45:26 2020

@author: seanmurphy
"""

from rhodium import * #import rhodium must be first line

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
# hedgetargets = np.ones((24*12,1))*150


def simulate(hedgetargets,
            strikeprice,
            HP = HubPricesConst,
            NP = NodePricesConst,
            WP = WindPowerConst,
            calendar=calendarConst):
    
            #set up empty vectors for values
            DeveloperProfits = 0
            TraderProfits = 0
            HedgeVarMetric = 0
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
                D = WP[i]*np.max((0,NP[i])) - np.max(hedgetargets[(month-1)*24+day_hour]-WP[i],0)*NP[i] + (strikeprice - HP[i])*hedgetargets[(month-1)*24+day_hour]
                DeveloperDaily = np.append(DeveloperDaily,D[0])
                DeveloperProfits = DeveloperProfits + D[0]
                T = (HP[i] - strikeprice)*hedgetargets[(month-1)*24+day_hour]
                TraderProfits = TraderProfits + T[0]

            
            #Minimum Annual profits
            Annual = np.zeros((years,1))
            for i in range(years):
                Annual[i] = np.sum(DeveloperDaily[i*365:i*365+365])
            DeveloperMinAnnual = np.min(Annual)
            
            #Hedge Targets
            for i in range(12):
                for j in range(23):
                    M = np.abs(hedgetargets[i*24+j+1] - hedgetargets[i*24+j])
                    # print(M)
                    HedgeVarMetric = HedgeVarMetric + M
        
            return DeveloperMinAnnual, HedgeVarMetric, DeveloperProfits, TraderProfits 

# a,b,c,d = simulate(hedgetargets,strikeprice,HP=HubPricesConst,NP=NodePricesConst,WP=WindPowerConst,calendar=calendarConst)

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

model.responses = [Response("DeveloperMinAnnual", Response.MAXIMIZE),
                  Response("HedgeVarMetric", Response.MINIMIZE),
                  Response("DeveloperProfits", Response.MAXIMIZE),
                  Response("TraderProfits", Response.MAXIMIZE)]

# constraints on outputs
    # not in the function yet, but i would recommend using this for:
        # generation meets hedge >= 90% of the time
    # given output of hedge goal satisfaction is "HedgeMet", format:
        # model.constraints = [Constraint("HedgeMet >= .9")]


# levers
    # (name, minimum, maximum, size)
    # I'm not sure what to do for upper limit on strike price
    
model.levers = [RealLever("hedgetargets", 0, 300, length = 288), # considering hedge target as 24 hour vectors each month
                RealLever("strikeprice", 18, 25, length = 1)]


# unused: model.uncertainties, could be useful for inputs currently considered as constants


# run model

nruns = 10000
out = optimize(model, "NSGAII", nruns)

# rhodium output data structures are a bit funky
    # all saved as csv
    # outputs are saved as numbers
    # input vectors are saved as strings, like:
        # "[1, 2, 3]"
    # if you want to plot the vector policies, you'll need custom plotters that convert string to vector
    
savepath = 'results.csv'
out.save(savepath)

# plt.plot(out.DeveloperMinAnnual, out.HedgeVarMetric)

df7 = pd.read_csv(savepath)
df7 = df7.sort_values(by = ['HedgeVarMetric']).reset_index()

plt.plot(df7.HedgeVarMetric, df7.DeveloperMinAnnual, c='b')

plt.xlabel('Hedge Var Metric')
plt.ylabel('Developer Min Annual ($)')

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)
