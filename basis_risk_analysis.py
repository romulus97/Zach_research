# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:00:54 2019

@author: jkern
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

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

#plot 2015 and 2016 nodal prices
plt.plot(RTN)
plt.xlabel('Hour')
plt.ylabel('Price $/MWh')
plt.show()

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

#plot 2015 and 2016 hub prices
plt.plot(RTH,color='r')
plt.xlabel('Hour')
plt.ylabel('Price $/MWh')
plt.show()

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

#plot 2015 and 2016 hub prices
plt.plot(WIND,color='g')
plt.xlabel('Hour')
plt.ylabel('Energy (MWh')
plt.show()

#########################################################################

# difference between hub price and node price
basis_difference = RTH - RTN

plt.scatter(WIND,basis_difference,c='orange',alpha=0.5,edgecolors='black')
plt.xlabel('Wind (MWh)')
plt.ylabel('Hub minus Node ($/MWh)')




