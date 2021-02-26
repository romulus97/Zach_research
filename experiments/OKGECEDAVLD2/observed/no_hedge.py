# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:17:44 2020

@author: jkern
"""

import numpy as np
import pandas as pd


def sim(HP, NP, WP, C,floor_months):
    
    #set up empty vectors for values
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
    mins = []
    
    strikeprice = 22.64
    
       
    for i in range(0,len(HP)):
        
        # what month, hour of the day is it?
        if i < 8760:
            j = i
        else:
            j = i%8760                    
        month = C[j,0]
        day_hour = C[j,2]
        
        # Peak or off-peak hour     
        if day_hour < 6 or day_hour > 21:
            p = 0
            
        else:  
            p = 1
        
        # Financial exchange
        D = float(WP[i]*max([0,NP[i]]))
        # DeveloperDaily = np.append(DeveloperDaily,D)
        DeveloperProfits += D
             
        # Monthly tracker
        if month != month_hold:
            month_hold = month
            Monthly.append(DeveloperMonth)
            
            if len(Monthly) <= floor_months:
                mins.append(DeveloperMonth)
            else:
                M = max(mins)
                if M > DeveloperMonth:
                    idx = mins.index(M)
                    mins[idx] = DeveloperMonth
            
            DeveloperMonth = D
                        
        else:
            DeveloperMonth += D

    
    # DeveloperHedge = np.float(DeveloperHedge)
    for i in range(0,len(Monthly)-1):
        MonthlyVar += abs(Monthly[i] - Monthly[i+1])
    MonthlyVar = -MonthlyVar
    
    VAR = sum(mins)


    return [DeveloperProfits, VAR, Monthly]
# print(results)
