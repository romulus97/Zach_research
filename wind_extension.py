# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 10:46:13 2020

@author: jkern
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from sklearn import linear_model

df_wind_2015 = pd.read_excel('wind_data.xlsx',sheet_name='2015',header=0)
df_wind_2016 = pd.read_excel('wind_data.xlsx',sheet_name='2016',header=0)

df_wind = df_wind_2015.append(df_wind_2016)
df_wind = df_wind.reset_index(drop=True)

wind_daily = []

days = int(len(df_wind)/24)

for i in range(0,days):
    
    daily = np.average(df_wind.loc[i*24:i*24+24,'MW'])
    wind_daily = np.append(wind_daily,daily)
    
df_OK_wind = pd.read_csv('OK_wind_data.csv',header=0)
df_OK_wind_selected = df_OK_wind.loc[0:729,'AWND']

#scatter plot of wind (x axis) and basis risk (y axis)
plt.scatter(df_OK_wind_selected,wind_daily,c='blue',alpha=0.3,edgecolors='black')
plt.xlabel('Wind Speeds')
plt.ylabel('Wind Power')
