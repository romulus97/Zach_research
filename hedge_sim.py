# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:17:44 2020

@author: jkern
"""

import numpy as np

def simulate(hedgetargets, 
             strikeprice,
             HP,
             NP,
             WP,
             calendar,
             ):
    
    #set up empty vectors for values
    volume = 25510
    DeveloperProfits = 0
    DeveloperHedge = 0
    DeveloperRevs = 0
    DeveloperMonth = 0
    TraderProfits = 0
    TraderRevs = 0
    DeveloperDaily = []
    Constraints = []
    Monthly = [] 
    month_hold = 1
    MonthlyVar = 0
    
       
    for i in range(0,len(HP)):
        
        # what month, hour of the day is it?
        if i < 8760:
            j = i
        else:
            j = i%8760                    
        month = calendar[j,0]
        day_hour = calendar[j,2]
        
        # Peak or off-peak hour     
        if day_hour < 6 or day_hour > 21:
            p = 0
            
        else:  
            p = 1
        
        # Financial exchange
        D = np.float(WP[i]*np.max([0,NP[i]]) - np.max([hedgetargets[(month-1)*2+p]-WP[i],0])*NP[i] + (strikeprice - HP[i])*hedgetargets[(month-1)*2+p])
        DeveloperProfits += D
        
        T = np.float((HP[i] - strikeprice)*hedgetargets[(month-1)*2+p])
        TraderRevs += np.max([0,T])
        # TraderProfits += T
        
        DH = np.float((strikeprice - HP[i])*hedgetargets[(month-1)*2+p])
        DeveloperRevs += np.max([0,DH])
 
        # Monthly tracker
        if month != month_hold:
            month_hold = month
            Monthly.append(DeveloperMonth)
            DeveloperMonth = D
        else:
            DeveloperMonth += D
    
    
    Ratio = np.float(TraderRevs/DeveloperRevs)
    # DeveloperHedge = np.float(DeveloperHedge)
    for i in range(0,len(Monthly)-1):
        MonthlyVar += np.abs(Monthly[i] - Monthly[i+1])
    MonthlyVar = -MonthlyVar
    
    return DeveloperProfits, Ratio, MonthlyVar
