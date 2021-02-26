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
    
fig, ((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12)) = plt.subplots(4,3,figsize=(8,7),sharey=True)

titles = ['MeanZero100Comparison_ObjectiveFunctions','MeanZero90Comparison_ObjectiveFunctions','MeanZero60Comparison_ObjectiveFunctions','MeanZero30Comparison_ObjectiveFunctions','StandardNormalComparison_ObjectiveFunctions','NoBasisRisk_Comparison_ObjectiveFunctions']

T = ['Mean Zero 100','Mean Zero 90','Mean Zero 60','Mean Zero 30','Standard Normal','No Basis Risk']

c = ['blue','orange','green','red','purple','gray']
C = {}
for color in c:
    idx = c.index(color)
    C[T[idx]] = color
    
for node in L: 
       
    n_index = L.index(node)
    ax = 'ax' + str(n_index+1)
    
    for t in titles:
        
        t_index = titles.index(t)
        tname = t + '.xlsx'

        df = pd.read_excel(tname,sheet_name = node, header=None,index_col=0)
        
        locals()[ax].plot(df.iloc[:,0],df.iloc[:,1]/1000,markeredgecolor=C[T[t_index]],markersize=3,markerfacecolor='None',marker='o',linestyle='None')
        # locals()[ax].set_xlabel('Fraction of Maximum Revenue',font='Arial',fontweight='bold')
        # locals()[ax].set_ylabel('Floor Improvement ($1000s)',font='Arial',fontweight='bold')
        locals()[ax].set_title(node,fontname = 'Arial',size=10)
    
    locals()[ax].set_ylim([0,800])
    locals()[ax].set_xlim([0.97,1])
    if n_index < 7:
        locals()[ax].set_xticks([])
        
    
        

ax11.set_visible(False)
ax12.set_visible(False)

fig.text(0.05, 0.5, 'Floor Improvement ($1000s)', fontname='Arial',fontweight='bold', va='center', rotation='vertical',size=14)
fig.text(0.35, 0.07, 'Fraction of Maximum Revenue', fontname='Arial',fontweight='bold', va='center',size=14)

plt.subplots_adjust(hspace=0.3,wspace=0.30)

plt.figlegend(T, loc = 'lower right', borderaxespad=0.1, ncol=2, labelspacing=0.34,  prop={'size': 10}, bbox_to_anchor=(.83,.15))  

plt.savefig('figureA3.png',dpi=500)
