# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 21:03:50 2021

@author: jkern
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import no_hedge


#pick nodal colors -- keep consistent with figure 3
df = pd.read_csv('monthly_prices.csv',header=0)

L = list(df.columns)
L = L[2:12]

c = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan']
C = {}
for color in c:
    idx = c.index(color)
    C[L[idx]] = color
    

# P99 hedgetargets
df_P99 = pd.read_excel('../P50.xlsx',sheet_name='hedge_targets',header=None)
P99 = df_P99.values
    
    
fig, ((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12)) = plt.subplots(4,3)

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

for node in L:
    
    filename = '../observed/' + node + '/observed/Decision_Variables.csv'
    df_D = pd.read_csv(filename, header=0,index_col=0)
    filename = '../observed/' + node + '/observed/Objective_Functions.csv'
    df_O  = pd.read_csv(filename, header=0,index_col=0)
    
    df_O.columns = ['Profits','F_change']
    order = range(0,len(df_O))
    df_O['order'] = order
    S = df_O.sort_values('Profits')
    pick = 0
    row_to_explore = S.iloc[pick,2]
    hedgetargets = df_D.iloc[row_to_explore,:].values
    
    peak = []
    offpeak = []
    w = 0.3
    x = np.array((range(1,13)))
    line_coords = []
    
    for i in range(0,12):
        offpeak.append(hedgetargets[i*2])
        peak.append(hedgetargets[i*2+1])
        line_coords.append(i-w+1)
        line_coords.append(i+1)
            
    ax = 'ax' + str(L.index(node)+1)

    locals()[ax].bar(x-w,offpeak,width=w,facecolor='dodgerblue',edgecolor='black',linewidth=.2,align='edge')
    locals()[ax].bar(x,peak,width=w,facecolor='deeppink',edgecolor = 'black',linewidth=.2,align='edge')
    locals()[ax].plot(line_coords,P99,color='gray',linestyle='--',linewidth=0.6)
    locals()[ax].set_title(node,fontname='Arial',size=7)
    locals()[ax].set_ylim([0,150])
    locals()[ax].set_xticks([1,2,3,4,5,6,7,8,9,10,11,12])
    locals()[ax].set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'],size=5)
    
    if L.index(node) == 0:
        # locals()[ax].set_xticks([])
        pass
    elif L.index(node) == 1:
        # locals()[ax].set_xticks([])
        locals()[ax].set_yticks([])
    elif L.index(node) == 2:
        # locals()[ax].set_xticks([])
        locals()[ax].set_yticks([])
    elif L.index(node) == 3:
        # locals()[ax].set_xticks([])
        pass
    elif L.index(node) == 4:
        # locals()[ax].set_xticks([])
        locals()[ax].set_yticks([])
    elif L.index(node) == 5:
        # locals()[ax].set_xticks([])
        locals()[ax].set_yticks([])        
    elif L.index(node) == 6:
        # locals()[ax].set_xticks([])
        pass        
    elif L.index(node) == 7:
        locals()[ax].set_yticks([])
    elif L.index(node) == 8:
        locals()[ax].set_yticks([])         

ax8.set_xlabel('Month',fontname = 'Arial',fontweight='bold')
# ax8.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12])
# ax8.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'],size=5)
ax9.set_xlabel('Month',fontname = 'Arial',fontweight='bold')
# ax9.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12])
# ax9.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'],size=5)
ax10.set_xlabel('Month',fontname = 'Arial',fontweight='bold') 
# ax10.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12])
# ax10.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'],size=5)     

ax11.set_visible(False)
ax12.set_visible(False)

plt.subplots_adjust(hspace=0.9,wspace=0.1)

fig.text(0.03, 0.5, 'Wind Power Production Targets (MWh)', fontname='Arial',fontweight='bold', va='center', rotation='vertical')

L = ['P99','Alternative Offpeak','Alternative Peak']
plt.figlegend(L, loc = 'lower right', borderaxespad=0.1, ncol=1, labelspacing=0.34,  prop={'size': 8}, bbox_to_anchor=(.76,.08))  

plt.savefig('figure8.png',dpi=500)

