# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:19:52 2019

@author: jkern
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from sklearn import linear_model

# read in excel file with price data
df_prices = pd.read_excel('SPP_LMPs.xlsx',sheet_name='Historical LMP',header=1)

# selecting only real time nodal prices for 2015
rtn2015 = df_prices['RT_NODE_2015']

# exclude the NAN values
rtn2015_edit = rtn2015.iloc[:8760]

# selecting only real time nodal prices for 2016
rtn2016 = df_prices['RT_NODE_2016']

# append 2015 and 2016 prices
rtn_both = rtn2015_edit.append(rtn2016)

# convert to numerical array
RTN = np.array(rtn_both)

#now do the same thing with hub prices
# selecting only real time hub prices for 2015
rth2015 = df_prices['RT_HUB_2015']

# exclude the NAN values
rth2015_edit = rth2015.iloc[:8760]

# selecting only real time hub prices for 2016
rth2016 = df_prices['RT_HUB_2016']

# append 2015 and 2016 prices
rth_both = rth2015_edit.append(rth2016)

# convert to numerical array
RTH = np.array(rth_both)

########################################################################

#now read in wind speed data

# read in excel file with wind speed data
df_wind = pd.read_excel('SPP_wind data_20180309.xlsx',sheet_name='Historical 8760s',header=14)

# selecting only wind power for 2015
wind2015 = df_wind['2015_MWh']

# exclude the NAN values
wind2015_edit = wind2015.iloc[:8760]

# selecting only wind power for 2016
wind2016 = df_wind['2016_MWh']

# append 2015 and 2016 wind power
wind_both = wind2015_edit.append(wind2016)

# convert to numerical array
WIND = np.array(wind_both)

#convert hourly wind data to daily
no_hours = len(WIND)
no_days = int(no_hours/24)
daily_total = []

for i in range(0,no_days):
    
    total = np.sum(WIND[i*24:i*24+24])
    
    daily_total.append(total)
    
#interpolate missing daily values
df_daily_total = pd.DataFrame(daily_total)
df_daily_total.columns = ['Daily_Total']

#interpolated daily wind data
fixed = df_daily_total.interpolate('linear') 

#fill in missing hourly wind data
for i in range(0,no_days):
    
    hourly_data = WIND[i*24:i*24+24]
    
    missing_hours = np.sum(np.isnan(hourly_data))
    
    if missing_hours == 1:
        
        # find location of missing hour
        location = np.where(np.isnan(hourly_data))
        location = location[0][0]
        
        # fill in value as mean of hour +/- 1
        WIND[i*24+location] = 0.5*WIND[i*24+location-1] + 0.5*WIND[i*24+location+1]

    elif missing_hours > 1:
        
        #daily total for the missing day
        DT = fixed.iloc[i,0]
        
        #find closest daily total on another day
        differences = abs(DT-fixed)
        sorted_differences = differences.sort_values(by='Daily_Total',ascending=True)
        val_mask = sorted_differences == sorted_differences.iloc[1,0]
        day = val_mask.index[val_mask['Daily_Total']==True][0]
        
        #take hourly data from that chosen day
        hourly = WIND[day*24:day*24+24]/np.sum(WIND[day*24:day*24+24])
        WIND[i*24:i*24+24] = hourly*DT
    else:
        pass
    
df_WIND = pd.DataFrame(WIND)
df_WIND.columns = ['Value']
df_WIND.to_csv('clean_WIND.csv')
        
    

