# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 21:03:50 2021

@author: jkern
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#pick nodal colors -- keep consistent with figure 3
df = pd.read_csv('monthly_prices.csv',header=0)

L = list(df.columns)
L = L[2:]

c = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan','black']
C = {}
for color in c:
    idx = c.index(color)
    C[L[idx]] = color
    
fig, ((ax1, ax2), (ax3,ax4)) = plt.subplots(2,2)

#figure 4

df = pd.read_csv('hourly_prices.csv',header=0)

L = list(df.columns)
L = L[1:]
   
font = {'fontname':'Arial'}

m = -375 #min
M = 1950 #max

# plot 5-year CDFs for each node

f = []

for node in L:
    s = df[node].values   
    p = np.ones((len(s),1))*(1/len(s))
    c = np.cumsum(p)
    r = np.sort(s)
    
    if node != 'SPP Hub':
        ax1.plot(r,c,color = C[node])
    else:
        ax1.plot(r,c,color = C[node],linestyle='--')

ax1.set_xlabel('Price ($/MWh',fontname='Arial',fontweight='bold')
ax1.set_ylabel('Cumulative Probability',fontname='Arial',fontweight='bold')
ax1.set_xlim(-100,250)
    

# monthly average prices
df = pd.read_csv('monthly_prices.csv',header=0)

L = list(df.columns)
L = L[2:]

for node in L:
    
    for year in [2015,2016,2017,2018,2019]:
        a = df.loc[df['Year']==year,node]
        a = a.reset_index(drop=True)
        if year == 2015:
            v = a
        else:
            v = v + a    
    if node != 'SPP Hub':
        ax2.plot(v,color = C[node])
    else:
        ax2.plot(v,color = C[node],linestyle='--')

ax2.set_xticks([0,3,6,9])
ax2.set_xticklabels(['Jan','Mar','Jul','Oct'])
ax2.set_xlabel('Month',fontname='Arial',fontweight = 'bold')
ax2.set_ylabel('Price ($/MWh',fontname='Arial',fontweight='bold')

ax4.set_visible(False)

plt.subplots_adjust(wspace=.35,hspace=0.4)

plt.figlegend(L, loc = 'lower center', borderaxespad=0.1, ncol=1, labelspacing=0.34,  prop={'size': 7}, bbox_to_anchor=(0.72,.085))  


# selected hourly prices
df = pd.read_csv('hourly_prices.csv',header=0)
N = ['OKGECEDAR5LD2','WFEC_MOORELAND_2','SPP Hub']

dates = list(df['Date'])
index = dates.index('4/20/2016 0:00')

for node in N:
    s = df.loc[index:index+168,node]
    s = s.reset_index(drop=True)
    if node != 'SPP Hub':
        ax3.plot(s,color=C[node],linewidth=.8)    
    else:
        ax3.plot(s,color=C[node],linestyle = '--')

ax3.set_xticks([0,72,144])
ax3.set_xticklabels(['4/20/17','4/23/17','4/26/17'])
ax3.set_xlabel('Date',fontname='Arial',fontweight = 'bold')
ax3.set_ylabel('Price ($/MWh',fontname='Arial',fontweight='bold')

plt.savefig('figure4.png',dpi=500)
