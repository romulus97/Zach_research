# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:27:27 2020

@author: jkern
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
df_data = pd.read_csv('input_data.csv', header=0)
data = df_data.loc[:,'Wind'].values
    
for i in range(0,5):
    
    sample = data[i*8760:i*8760+8760]
    
    if i < 1:
    
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
        nov = sample[24*304:24*334]
        dec = sample[24*334:24*365]
        
        JA = jan
        FE = feb
        MR = mar
        AP = apr
        MA = may
        JN = jun
        JL = jul
        AU = aug
        SE = sep
        OC = octo
        NO = nov
        DE = dec
    
    else:
        
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
        nov = sample[24*304:24*334]
        dec = sample[24*334:24*365]
        
        JA = np.append(JA,jan)
        FE = np.append(FE,feb)
        MR = np.append(MR,mar)
        AP = np.append(AP,apr)
        MA = np.append(MA,may)
        JN = np.append(JN,jun)
        JL = np.append(JL,jul)
        AU = np.append(AU,aug)
        SE = np.append(SE,sep)
        OC = np.append(OC,octo)
        NO = np.append(NO,nov)
        DE = np.append(DE,dec) 
    
janM = vector2matrix(JA)
febM= vector2matrix(FE)
marM = vector2matrix(MR)
aprM = vector2matrix(AP)
mayM = vector2matrix(MA)
junM = vector2matrix(JN)
julM = vector2matrix(JL)
augM = vector2matrix(AU)
sepM = vector2matrix(SE)
octM = vector2matrix(OC)
novM = vector2matrix(NO)
decM = vector2matrix(DE)
  
for i in range(0,24):
        
        targets[0,i] = np.median(janM[:,i])
        targets[1,i] = np.median(febM[:,i])
        targets[2,i] = np.median(marM[:,i])
        targets[3,i] = np.median(aprM[:,i])
        targets[4,i] = np.median(mayM[:,i])
        targets[5,i] = np.median(junM[:,i])
        targets[6,i] = np.median(julM[:,i])
        targets[7,i] = np.median(augM[:,i])
        targets[8,i] = np.median(sepM[:,i])
        targets[9,i] = np.median(octM[:,i])
        targets[10,i] = np.median(novM[:,i])
        targets[11,i] = np.median(decM[:,i])
            
T_targets = np.transpose(targets)

plt.figure()
plt.plot(T_targets)
plt.xlabel('Hour')
plt.ylabel('Wind Power (MWh)')
# plt.legend(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],framealpha=1)
plt.savefig('diurnal.png',dpi=500)

df_T = pd.DataFrame(T_targets)
df_T.columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
df_T.to_excel('P50.xlsx')



           
        
    
    
    