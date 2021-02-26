# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 21:03:50 2021

@author: jkern
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#figure 3

df = pd.read_csv('monthly_prices.csv',header=0)

L = list(df.columns)
L = L[2:]

#pick nodal colors
c = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan','black']
C = {}
for color in c:
    idx = c.index(color)
    C[L[idx]] = color
    
font = {'fontname':'Arial'}

#plot monthly average prices for each year

fig, ((ax1, ax2, ax3), (ax4,ax5,ax6)) = plt.subplots(2,3)

#2015
for node in L:
    a = df.loc[df['Year']==2015,node]
    a = a.reset_index(drop=True)
    if node != 'SPP Hub':
        ax1.plot(a,color = C[node])
    else:
        ax1.plot(a,color = C[node],linestyle='--')
ax1.set_title('2015',fontname='Arial',fontweight='bold')
ax1.set_xticks([])
ax1.set_ylabel('Price ($/MWh',fontname='Arial',fontweight='bold')

#2016
for node in L:
    a = df.loc[df['Year']==2016,node]
    a = a.reset_index(drop=True)
    if node != 'SPP Hub':
        ax2.plot(a,color = C[node])
    else:
        ax2.plot(a,color = C[node],linestyle='--')
ax2.set_title('2016',fontname='Arial',fontweight='bold')
ax2.set_xticks([])
    
#2017
for node in L:
    a = df.loc[df['Year']==2017,node]
    a = a.reset_index(drop=True)
    if node != 'SPP Hub':
        ax3.plot(a,color = C[node])
    else:
        ax3.plot(a,color = C[node],linestyle='--')
ax3.set_title('2017',fontname='Arial',fontweight='bold')
ax3.set_xticks([0,3,6,9])
ax3.set_xticklabels(['Jan','Mar','Jul','Oct'])

#2018
for node in L:
    a = df.loc[df['Year']==2018,node]
    a = a.reset_index(drop=True)
    if node != 'SPP Hub':
        ax4.plot(a,color = C[node])
    else:
        ax4.plot(a,color = C[node],linestyle='--')
ax4.set_title('2018',fontname='Arial',fontweight='bold')
ax4.set_xlabel('Month',fontname='Arial',fontweight='bold')
ax4.set_ylabel('Price ($/MWh',fontname='Arial',fontweight='bold')
ax4.set_xticks([0,3,6,9])
ax4.set_xticklabels(['Jan','Mar','Jul','Oct'])

#2019
for node in L:
    a = df.loc[df['Year']==2019,node]
    a = a.reset_index(drop=True)
    if node != 'SPP Hub':
        ax5.plot(a,color = C[node])
    else:
        ax5.plot(a,color = C[node],linestyle='--')
ax5.set_title('2019',fontname='Arial',fontweight='bold')
ax5.set_xlabel('Month',fontname='Arial',fontweight='bold')
ax5.set_xticks([0,3,6,9])
ax5.set_xticklabels(['Jan','Mar','Jul','Oct'])

ax6.set_visible(False)

plt.subplots_adjust(wspace=.3)
plt.figlegend(L, loc = 'lower center', borderaxespad=0.1, ncol=1, labelspacing=0.34,  prop={'size': 7}, bbox_to_anchor=(0.8,.1))  

plt.savefig('figure3.png',dpi=500)
