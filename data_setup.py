# -*- coding: utf-8 -*-
"""
Created on Wed May 03 15:01:31 2017

@author: jdkern
"""

import pandas as pd
import numpy as np


##time series of load for each zone
df_prices = pd.read_excel('hourly_inputs.xlsx',header=0)  

#write data.dat file
filename = 'data.dat'
with open(filename, 'w') as f:
    
################
#  parameters  #
################
    
    # simulation details
    f.write('param MW := %d;' % 10)
    f.write('\n')
    f.write('param MWh:= %d;' % 40)
    f.write('\n\n')
    
    # times series data
    # zonal (hourly)
    f.write('param:' + '\t' + 'RT_node:=' + '\n')      
    for h in range(0,len(df_prices)): 
            f.write(str(h) + '\t' + str(df_prices.loc[h,'RT_node']) + '\n')
    f.write(';\n\n')