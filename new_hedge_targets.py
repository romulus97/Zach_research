# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:27:27 2020

@author: jkern
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('stoch_wind.csv',header=0,index_col=0)

num_years = int(len(data)/8760)

targets = np.zeros((12,24))

###################################33

def vector2matrix(v):
    
    r = int(len(v)/24)
    m = np.zeros((r,24))
    
    for i in range(0,r):
        
        for j in range(0,24):
        
            m[i,j] = v[i*24+j]
    
    return m

######################################

for i in range(0,num_years):
    
    sample = data.loc[i*8760:i*8760+8759].values
    
    jan = sample[0:24*31]
    feb = sample[24*31:24*59]
    mar = sample[24*59:24*90]
    apr = sample[24*90:24*120]
    may = sample[24*120:24*151]
    jun = sample[24*151:24*181]
    jul = sample[24*181:24*212]
    aug = sample[24*212:24*243]
    sep = sample[24*243:24*273]
    octo = sample[24*273:24*304]
    nov = sample[24*304:24*335]
    dec = sample[24*335:24*365]
    
    janM = vector2matrix(jan)
    febM= vector2matrix(feb)
    marM = vector2matrix(mar)
    aprM = vector2matrix(apr)
    mayM = vector2matrix(may)
    junM = vector2matrix(jun)
    julM = vector2matrix(jul)
    augM = vector2matrix(aug)
    sepM = vector2matrix(sep)
    octM = vector2matrix(octo)
    novM = vector2matrix(nov)
    decM = vector2matrix(dec)
  
    for i in range(0,24):
            
            targets[0,i] = targets[0,i] + np.mean(janM[:,i])
            targets[1,i] = targets[1,i] + np.mean(febM[:,i])
            targets[2,i] = targets[2,i] + np.mean(marM[:,i])
            targets[3,i] = targets[3,i] + np.mean(aprM[:,i])
            targets[4,i] = targets[4,i] + np.mean(mayM[:,i])
            targets[5,i] = targets[5,i] + np.mean(junM[:,i])
            targets[6,i] = targets[6,i] + np.mean(julM[:,i])
            targets[7,i] = targets[7,i] + np.mean(augM[:,i])
            targets[8,i] = targets[8,i] + np.mean(sepM[:,i])
            targets[9,i] = targets[9,i] + np.mean(octM[:,i])
            targets[10,i] = targets[10,i] + np.mean(novM[:,i])
            targets[11,i] = targets[11,i] + np.mean(decM[:,i])
            
targets = targets/num_years

T_targets = np.transpose(targets)

plt.figure()
plt.plot(T_targets)
plt.xlabel('Hour')
plt.ylabel('Target (MWh)')




           
        
    
    
    