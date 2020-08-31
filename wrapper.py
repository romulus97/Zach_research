# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:14:07 2017

@author: YSu
"""

from pyomo.opt import SolverFactory
from hedge_target_optimizer import model
from pyomo.core import Var
from pyomo.core import Param
from operator import itemgetter
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import traceback

instance = model.create_instance('data.dat')

opt = SolverFactory("cplex")

#Space to store results
      
try:
    results = opt.solve(instance,tee=True)
    instance.solutions.load_from(results)
except Exception:
    print('Solve encountered an error:', sys.exc_info()[0])
    traceback.print_exc() 

jan = []
feb = []
mar = []
apr = []
may = []
jun = []
jul = []
aug = []
sep = []
octo = []
nov = []
dec = []
 
#The following section is for storing and sorting results
for v in instance.component_objects(Var, active=True):
    varobject = getattr(instance, str(v))
    a=str(v)
    if a=='jan':
     
     for index in varobject:
         if index in instance.jan:
             jan.append(varobject[index].value)
        

    elif a=='feb':
     
     for index in varobject:         
         if index in instance.feb:             
             feb.append(varobject[index].value)



    elif a=='mar':
     
     for index in varobject:         
         if index in instance.mar:             
             mar.append(varobject[index].value)
             

    elif a=='apr':
     
     for index in varobject:         
         if index in instance.apr:             
             apr.append(varobject[index].value)


    elif a=='may':
     
     for index in varobject:         
         if index in instance.may:             
             may.append(varobject[index].value)
             
             

    elif a=='jun':
     
     for index in varobject:
         if index in instance.jun:             
             jun.append(varobject[index].value)
             

    elif a=='jul':
     
     for index in varobject:         
         if index in instance.jul:
             jul.append(varobject[index].value)
             
             

    elif a=='aug':
     
     for index in varobject:         
         if index in instance.aug:             
             aug.append(varobject[index].value)


    elif a=='sep':
     
     for index in varobject:         
         if index in instance.sep:             
             sep.append(varobject[index].value)


    elif a=='oct':
     
     for index in varobject:         
         if index in instance.oct:             
             octo.append(varobject[index].value)


    elif a=='nov':
     
     for index in varobject:         
         if index in instance.nov:             
             nov.append(varobject[index].value)
             


    elif a=='dec':
     
     for index in varobject:         
         if index in instance.dec:             
             dec.append(varobject[index].value)
             
             

#        for index in varobject:
#            
#            if index in instance.charge:
#             
#             C.append([index,varobject[index].value*0.8])
            
##                         
#discharge_pd=pd.DataFrame(D,columns=('Hour','MWh'))
#charge_pd=pd.DataFrame(C,columns=('Hour','MWh'))
#
#discharge_pd.to_csv('discharge.csv')
#charge_pd.to_csv('charge.csv')

targets = np.column_stack((jan,feb,mar,apr,may,jun,jul,aug,sep,octo,nov,dec))
df_targets = pd.DataFrame(targets)
df_targets.columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
df_targets.to_csv('optimized_targets.csv')
