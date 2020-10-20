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
OK_wind_selected = df_OK_wind.loc[0:729,'AWND'].values

#scatter plot of wind (x axis) and basis risk (y axis)
plt.scatter(OK_wind_selected,wind_daily,c='blue',alpha=0.3,edgecolors='black')
plt.xlabel('Wind Speeds')
plt.ylabel('Wind Power')

#break data down into bins
averages = np.zeros((31,1))
stds = np.zeros((31,1))

for i in range(0,31):
    a = wind_daily[(OK_wind_selected < i + 1) & (OK_wind_selected > i)]
    averages[i] = np.mean(a)
    stds[i] = np.std(a)

# correct for NaNs
averages[0] = averages[3]
averages[1] = averages[3]
averages[2] = averages[3]
averages[26] = averages[27]
averages[28] = averages[30]
averages[29] = averages[30]

stds[0] = stds[3]
stds[1] = stds[3]
stds[2] = stds[3]
stds[26] = stds[27]
stds[28] = stds[30]
stds[29] = stds[30]

    
#convert new OK wind data to daily wind power
OK_wind_new = df_OK_wind.loc[730:,'AWND'].values

new_wind_daily = []
for i in range(0,len(OK_wind_new)):
    idx = int(min(np.round(OK_wind_new[i]),30))
    new = max(0,np.random.normal(0,1)*stds[idx] + averages[idx])
    new_wind_daily.append(new)
    
#sample hourly values from 2013-2016 values
df_wind_2013 = pd.read_excel('wind_data.xlsx',sheet_name='2013',header=0)
df_wind_2014 = pd.read_excel('wind_data.xlsx',sheet_name='2014',header=0)
df_wind_2015 = pd.read_excel('wind_data.xlsx',sheet_name='2015',header=0)
df_wind_2016 = pd.read_excel('wind_data.xlsx',sheet_name='2016',header=0)

df_wind = df_wind_2013.append(df_wind_2014)
df_wind = df_wind.append(df_wind_2015)
df_wind = df_wind.append(df_wind_2016)
df_wind = df_wind.reset_index(drop=True)

wind_daily = []

days = int(len(df_wind)/24)

for i in range(0,days):
    
    daily = np.average(df_wind.loc[i*24:i*24+24,'MW'])
    wind_daily = np.append(wind_daily,daily)

new_wind_hourly = np.zeros((len(new_wind_daily)*24,1))

for i in range(0,len(new_wind_daily)):
    
    daily_MW = new_wind_daily[i]
    MW_difference = np.abs(wind_daily - daily_MW)
    df_daily_difference = pd.DataFrame()
    df_daily_difference['Order'] = range(0,len(wind_daily))
    df_daily_difference['MW'] = MW_difference
    df_sorted = df_daily_difference.sort_values(by='MW',axis=0,ascending=True)
    idx = df_sorted.iloc[0,0]
    
    a = df_wind.loc[idx*24:idx*24+23,'MW'].values
    a = np.reshape(a,(24,1))
    new_wind_hourly[i*24:i*24+24] = a
    
df_hourly_new = pd.DataFrame(new_wind_hourly)
df_hourly_new.to_excel('hourly_2017_2019.xlsx')

    