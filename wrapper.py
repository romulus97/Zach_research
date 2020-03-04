# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:14:07 2017

@author: YSu
"""

from pyomo.opt import SolverFactory
from battery_dispatch import model
from pyomo.core import Var
from pyomo.core import Param
from operator import itemgetter
import pandas as pd
import numpy as np
from datetime import datetime

instance = model.create_instance('data.dat')

opt = SolverFactory("cplex")

#Space to store results
      
result = opt.solve(instance)
instance.solutions.load_from(result)   

D = []
C = []
S = []
 
#The following section is for storing and sorting results
for v in instance.component_objects(Var, active=True):
    varobject = getattr(instance, str(v))
    a=str(v)
    if a=='discharge':
     
     for index in varobject:
         
         if index in instance.discharge:
             
             D.append([index,varobject[index].value])
        
    elif a=='charge':
    
        for index in varobject:
            
            if index in instance.charge:
             
             C.append([index,varobject[index].value*0.8])
#                         
discharge_pd=pd.DataFrame(D,columns=('Hour','MWh'))
charge_pd=pd.DataFrame(C,columns=('Hour','MWh'))

discharge_pd.to_csv('discharge.csv')
charge_pd.to_csv('charge.csv')


