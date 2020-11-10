# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 21:19:45 2020

@author: jkern
"""

import pandas as pd
import os
import numpy as np
from shutil import copy
from pathlib import Path


#####################################################################
##########              BASIS RISK SCENARIO        ########################
#####################################################################

# import constant inputs
df_data = pd.read_csv('input_data.csv', header=0)
X = df_data.values
HubPrices = X[:,0]
WindPower = X[:,2]

# import node prices
df_node = pd.read_csv('ten_more_nodes.csv',header=None)
df_node.fillna('ffill')
N = df_node.values

nodes = ['WFECVICILD2','OKGEIODINE4LD2','OKGEWDWRD1LD2','OKGEWDWRDEHVUNKEENAN_WIND','OKGEKEENANWIND','OKGECEDAR5LD2','OKGESPIRITWIND','OKGE_SEILING','OKGECEDAVLD2','WFEC_MOORELAND_2']
scenarios = ['no_basis_risk','std_normal','mean_zero_10p_std','mean_zero_20p_std','mean_zero_30p_std','mean_zero_40p_std','mean_zero_50p_std','mean_zero_60p_std','mean_zero_70p_std','mean_zero_80p_std','mean_zero_90p_std','mean_zero']

for n in nodes:
    
    idx = nodes.index(n)
    NodePrices = N[:,idx]
    
    for s in scenarios:
        
        B = []
        
        path=str(Path.cwd()) +str(Path('/experiments/' + n + '/' + s))
        os.makedirs(path,exist_ok=True)
        
        for j in range(0,len(NodePrices)):
            
            B.append(NodePrices[j] - HubPrices[j])

        bias = np.mean(B)
        spread = np.std(B)
        BasisRisk = np.array(B)
        
        if s == 'mean_zero':
            BasisRisk = BasisRisk - bias
        elif s == 'mean_zero_10p_std':
            BasisRisk = (BasisRisk - bias)/((spread*.90))
        elif s == 'mean_zero_20p_std':
            BasisRisk = (BasisRisk - bias)/((spread*(1-.20)))
        elif s == 'mean_zero_30p_std':
            BasisRisk = (BasisRisk - bias)/((spread*(1-.30)))    
        elif s == 'mean_zero_40p_std':
            BasisRisk = (BasisRisk - bias)/((spread*(1-.40)))   
        elif s == 'mean_zero_50p_std':
            BasisRisk = (BasisRisk - bias)/((spread*(1-.50)))
        elif s == 'mean_zero_60p_std':
            BasisRisk = (BasisRisk - bias)/((spread*(1-.60)))
        elif s == 'mean_zero_70p_std':
            BasisRisk = (BasisRisk - bias)/((spread*(1-.70)))
        elif s == 'mean_zero_80p_std':
            BasisRisk = (BasisRisk - bias)/((spread*(1-.80)))   
        elif s == 'mean_zero_90p_std':
            BasisRisk = (BasisRisk - bias)/((spread*(1-.90)))
        elif s == 'std_normal':
            BasisRisk = (BasisRisk - bias)/((spread))
        elif s == 'no_basis_risk':
            BasisRisk = 0
            
        P = HubPrices + BasisRisk
        
        inputs = np.column_stack((HubPrices,P,WindPower))
        df_inputs = pd.DataFrame(inputs)
        df_inputs.columns = ['HubPrices','NodePrices','WindPower']
        fn = 'experiments/' + n + '/' + s + '/input_data.csv'
        df_inputs.to_csv(fn,index=False)
        

        no_hedge = 'no_hedge.py'
        model = 'platypus_hedge_model.py'
        calendar = 'calendar.csv'

        copy(no_hedge,path)
        copy(model,path)
        copy(calendar,path) 
    
    
