# -*- coding: utf-8 -*-
"""
Created on Wed May 03 15:01:31 2017

@author: jdkern
"""

import pandas as pd
import numpy as np


# Hub prices
HubPrices = pd.read_csv('stoch_hub.csv',header=0,index_col=0)
HubPrices = HubPrices.values

# Node prices
NodePrices = pd.read_csv('stoch_nodal.csv',header=0,index_col=0)
NodePrices = NodePrices.values

# Wind power production
WindPower = pd.read_csv('stoch_wind.csv',header=0,index_col=0)
WindPower = WindPower.values

years = 2
#years = 30 #default
hours = int(years*8760)


#write data.dat file
filename = 'data.dat'
with open(filename, 'w') as f:
    
################
#  parameters  #
################
    
    f.write('param Strike:= 23')
    f.write(';\n\n')
    
    #system wide (daily)
    f.write('param:' + '\t' + 'RT_node' + '\t' + 'RT_hub' + '\t' + 'Wind:=' + '\n')
#    for d in range(0,len(HubPrices)):
    
    for d in range(0,hours):
            f.write(str(d) + '\t' + str(float(NodePrices[d])) + '\t' + str(float(HubPrices[d])) + '\t' + str(float(WindPower[d])) + '\n')
    f.write(';\n\n')
    
    
#    # simulation details
#    f.write('param MW := %d;' % 10)
#    f.write('\n')
#    f.write('param MWh:= %d;' % 40)
#    f.write('\n\n')
#    
#    # times series data
#    # zonal (hourly)
#    f.write('param:' + '\t' + 'RT_node:=' + '\n')      
#    for h in range(0,len(df_prices)): 
#            f.write(str(h) + '\t' + str(df_prices.loc[h,'RT_node']) + '\n')
#    f.write(';\n\n')