# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 15:21:28 2020

@author: jkern
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
from sklearn import linear_model

# read in clean wind data
df_wind = pd.read_csv('clean_WIND.csv')

# read in demand data
df_demand = pd.read_csv('clean_DEMAND.csv')

#read in price data
df_prices = pd.read_csv('clean_HUB_PRICES.csv')

#
# Generate 30 years of stochastic data
years = 30

stoch_wind = np.zeros((years*8760,1))
stoch_demand = np.zeros((years*8760,1))
stoch_HUB = np.zeros((years*8760,1))

# remove leap days from observed data
start_wind = df_wind.loc[0:8760+24*(31+28)-1,'Value']
end_wind = df_wind.loc[8760+24*(31+28+1):,'Value']
df_combined_wind = start_wind.append(end_wind)

start_demand = df_demand.loc[0:8760+24*(31+28)-1,'Value']
end_demand = df_demand.loc[8760+24*(31+28+1):,'Value']
df_combined_demand = start_demand.append(end_demand)

start_prices = df_prices.loc[0:8760+24*(31+28)-1,'Value']
end_prices = df_prices.loc[8760+24*(31+28+1):,'Value']
df_combined_prices = start_prices.append(end_prices)

for i in range(0,int(years/2)):
    stoch_wind[i*17520:i*17520+17520,0] = df_combined_wind.loc[:]
    stoch_demand[i*17520:i*17520+17520,0] = df_combined_demand.loc[:]
    stoch_HUB[i*17520:i*17520+17520,0] = df_combined_prices.loc[:]

# use regression and error sampling to create record of basis risk
#regression model to predict basis risk
coef_1 = 1.42532468e-01
coef_2 = -2.30879077e-05
intercept = 3.715569787261286

# best fit distribution: st.cauchy
best_fit_params = [8.929849945,8.0275377602]

basis_risk = []
nodal_prices = []

for i in range(0,len(stoch_HUB)):
    
    print(i)
    
    y_hat = stoch_wind[i]*coef_1 + stoch_demand[i]*coef_2 + intercept
    
    # add random sample from error distribution
    count = 0
    
    e = st.cauchy.rvs(loc=best_fit_params[0], scale=best_fit_params[1], size=1)
    
    while e > 45 or e < -700:
        e = st.cauchy.rvs(loc=best_fit_params[0], scale=best_fit_params[1], size=1)
        count = count + 1
        
        if count > 100:
            e = 0
            break
        
    basis_risk = np.append(basis_risk,y_hat - e)
    
    nodal_prices = np.append(nodal_prices, -1*(y_hat - e - stoch_HUB[i]))
    
df_nodal = pd.DataFrame(nodal_prices)
df_nodal.to_csv('stoch_nodal.csv')
df_wind = pd.DataFrame(stoch_wind)
df_wind.to_csv('stoch_wind.csv')
df_demand = pd.DataFrame(stoch_demand)
df_demand.to_csv('stoch_demand.csv')
df_hub = pd.DataFrame(stoch_HUB)
df_hub.to_csv('stoch_hub.csv')

    