# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 21:03:50 2021

@author: jkern
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import no_hedge


#pick nodal colors -- keep consistent with figure 3
df = pd.read_csv('monthly_prices.csv',header=0)

L = list(df.columns)
L = L[2:12]

c = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan']
C = {}
for color in c:
    idx = c.index(color)
    C[L[idx]] = color
    
fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(8,7),sharex=True,sharey=True)

titles = ['MeanZero100Comparison_ObjectiveFunctions','MeanZero90Comparison_ObjectiveFunctions','MeanZero60Comparison_ObjectiveFunctions','MeanZero30Comparison_ObjectiveFunctions','StandardNormalComparison_ObjectiveFunctions','NoBasisRisk_Comparison_ObjectiveFunctions']

T = ['Mean Zero 100','Mean Zero 90','Mean Zero 60','Mean Zero 30','Standard Normal','No Basis Risk']

for t in titles:
    
    t_index = titles.index(t)
    tname = t + '.xlsx'
    ax = 'ax' + str(t_index+1)
    
    for node in L:
        
        df = pd.read_excel(tname,sheet_name = node, header=None,index_col=0)
        
        locals()[ax].plot(df.iloc[:,0],df.iloc[:,1]/1000,markeredgecolor=C[node],markersize=3,markerfacecolor='None',marker='o',linestyle='None')
        # locals()[ax].set_xlabel('Fraction of Maximum Revenue',font='Arial',fontweight='bold')
        # locals()[ax].set_ylabel('Floor Improvement ($1000s)',font='Arial',fontweight='bold')
        locals()[ax].set_title(T[t_index],fontname = 'Arial',size=12)

fig.text(0.05, 0.5, 'Floor Improvement ($1000s)', fontname='Arial',fontweight='bold', va='center', rotation='vertical',size=14)
fig.text(0.35, 0.07, 'Fraction of Maximum Revenue', fontname='Arial',fontweight='bold', va='center',size=14)

plt.subplots_adjust(hspace=0.2,wspace=0.2)

plt.figlegend(L, loc = 'upper center', borderaxespad=0.1, ncol=3, labelspacing=0.34,  prop={'size': 7}, bbox_to_anchor=(0.5,1.0))  

plt.savefig('figure9.png',dpi=500)
