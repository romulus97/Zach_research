# -*- coding: utf-8 -*-
"""
Created on Fri Jul 07 12:23:45 2017

@author: jdkern
"""

#######################################################################################################
# a basic unit commitment model for CAISO system                                                       #
# This is the trial version of the electricity market model                                            #
# 4 Zone system                                                                                        #                                                                                #
#######################################################################################################


from __future__ import division # This line is used to ensure that int or long division arguments are converted to floating point values before division is performed 
from pyomo.environ import * # This command makes the symbols used by Pyomo known to Python
from pyomo.opt import SolverFactory
import itertools

##Create a solver
opt = SolverFactory('cplex')

model = AbstractModel()

# Operating horizon information 
years = 2
model.Hours = RangeSet(0,17519)
model.Wind = Param(model.Hours, within=Reals)
model.RT_node = Param(model.Hours, within=Reals)
model.RT_hub = Param(model.Hours,within=Reals)
model.h = RangeSet(0,23)


# create monthly day sets

def Jan_init(model):    
        for i in range(0,31):
            for j in range(0,years):
                yield i + 365*j      
model.jan_days = Set(initialize=Jan_init)

def Feb_init(model):    
        for i in range(31,59):
            for j in range(0,years):
                yield i + 365*j        
model.feb_days = Set(initialize=Feb_init)

def Mar_init(model):    
        for i in range(59,90):
            for j in range(0,years):
                yield i + 365*j        
model.mar_days = Set(initialize=Mar_init)

def Apr_init(model):    
        for i in range(90,120):
            for j in range(0,years):
                yield i + 365*j        
model.apr_days = Set(initialize=Apr_init)

def May_init(model):    
        for i in range(120,151):
            for j in range(0,years):
                yield i + 365*j        
model.may_days = Set(initialize=May_init)

def June_init(model):    
        for i in range(151,181):
            for j in range(0,years):
                yield i + 365*j        
model.jun_days = Set(initialize=June_init)

def July_init(model):    
        for i in range(181,212):
            for j in range(0,years):
                yield i + 365*j        
model.jul_days = Set(initialize=July_init)

def Aug_init(model):    
        for i in range(212,243):
            for j in range(0,years):
                yield i + 365*j        
model.aug_days = Set(initialize=Aug_init)

def Sep_init(model):    
        for i in range(243,273):
            for j in range(0,years):
                yield i + 365*j        
model.sep_days = Set(initialize=Sep_init)

def Oct_init(model):    
        for i in range(273,304):
            for j in range(0,years):
                yield i + 365*j        
model.oct_days = Set(initialize=Oct_init)

def Nov_init(model):    
        for i in range(304,334):
            for j in range(0,years):
                yield i + 365*j        
model.nov_days = Set(initialize=Nov_init)

def Dec_init(model):    
        for i in range(334,365):
            for j in range(0,years):
                yield i + 365*j        
model.dec_days = Set(initialize=Dec_init)

###########################################################
### Hedge Model Section
###########################################################

model.Strike = Param(within=NonNegativeReals)

# Wind dispatch
model.WindDispatch = Var(model.Hours, within=NonNegativeReals,initialize=0)

# Hedge Targets
model.jan = Var(model.h, within=NonNegativeReals,initialize=0)
model.feb = Var(model.h, within=NonNegativeReals,initialize=0)
model.mar = Var(model.h, within=NonNegativeReals,initialize=0)
model.apr = Var(model.h, within=NonNegativeReals,initialize=0)
model.may = Var(model.h, within=NonNegativeReals,initialize=0)
model.jun = Var(model.h, within=NonNegativeReals,initialize=0)
model.jul = Var(model.h, within=NonNegativeReals,initialize=0)
model.aug = Var(model.h, within=NonNegativeReals,initialize=0)
model.sep = Var(model.h, within=NonNegativeReals,initialize=0)
model.oct = Var(model.h, within=NonNegativeReals,initialize=0)
model.nov = Var(model.h, within=NonNegativeReals,initialize=0)
model.dec = Var(model.h, within=NonNegativeReals,initialize=0)

model.jan_short = Var(model.jan_days, model.h, within=NonNegativeReals,initialize=0)
model.feb_short = Var(model.feb_days, model.h, within=NonNegativeReals,initialize=0)
model.mar_short = Var(model.mar_days, model.h, within=NonNegativeReals,initialize=0)
model.apr_short = Var(model.apr_days, model.h, within=NonNegativeReals,initialize=0)
model.may_short = Var(model.may_days, model.h, within=NonNegativeReals,initialize=0)
model.jun_short = Var(model.jun_days, model.h, within=NonNegativeReals,initialize=0)
model.jul_short = Var(model.jul_days, model.h, within=NonNegativeReals,initialize=0)
model.aug_short = Var(model.aug_days, model.h, within=NonNegativeReals,initialize=0)
model.sep_short = Var(model.sep_days, model.h, within=NonNegativeReals,initialize=0)
model.oct_short = Var(model.oct_days, model.h, within=NonNegativeReals,initialize=0)
model.nov_short = Var(model.nov_days, model.h, within=NonNegativeReals,initialize=0)
model.dec_short = Var(model.dec_days, model.h, within=NonNegativeReals,initialize=0)


model.jan_contract_charge = Var(model.jan_days, model.h, within=NonNegativeReals,initialize=0)
model.feb_contract_charge = Var(model.feb_days, model.h, within=NonNegativeReals,initialize=0)
model.mar_contract_charge = Var(model.mar_days, model.h, within=NonNegativeReals,initialize=0)
model.apr_contract_charge = Var(model.apr_days, model.h, within=NonNegativeReals,initialize=0)
model.may_contract_charge = Var(model.may_days, model.h, within=NonNegativeReals,initialize=0)
model.jun_contract_charge = Var(model.jun_days, model.h, within=NonNegativeReals,initialize=0)
model.jul_contract_charge = Var(model.jul_days, model.h, within=NonNegativeReals,initialize=0)
model.aug_contract_charge = Var(model.aug_days, model.h, within=NonNegativeReals,initialize=0)
model.sep_contract_charge = Var(model.sep_days, model.h, within=NonNegativeReals,initialize=0)
model.oct_contract_charge = Var(model.oct_days, model.h, within=NonNegativeReals,initialize=0)
model.nov_contract_charge = Var(model.nov_days, model.h, within=NonNegativeReals,initialize=0)
model.dec_contract_charge = Var(model.dec_days, model.h, within=NonNegativeReals,initialize=0)


model.jan_contract_payout = Var(model.jan_days, model.h, within=NonNegativeReals,initialize=0)
model.feb_contract_payout = Var(model.feb_days, model.h, within=NonNegativeReals,initialize=0)
model.mar_contract_payout = Var(model.mar_days, model.h, within=NonNegativeReals,initialize=0)
model.apr_contract_payout = Var(model.apr_days, model.h, within=NonNegativeReals,initialize=0)
model.may_contract_payout = Var(model.may_days, model.h, within=NonNegativeReals,initialize=0)
model.jun_contract_payout = Var(model.jun_days, model.h, within=NonNegativeReals,initialize=0)
model.jul_contract_payout = Var(model.jul_days, model.h, within=NonNegativeReals,initialize=0)
model.aug_contract_payout = Var(model.aug_days, model.h, within=NonNegativeReals,initialize=0)
model.sep_contract_payout = Var(model.sep_days, model.h, within=NonNegativeReals,initialize=0)
model.oct_contract_payout = Var(model.oct_days, model.h, within=NonNegativeReals,initialize=0)
model.nov_contract_payout = Var(model.nov_days, model.h, within=NonNegativeReals,initialize=0)
model.dec_contract_payout = Var(model.dec_days, model.h, within=NonNegativeReals,initialize=0)

####################################################################
##Objective function                                               #
##To minimize overall system cost while satistfy system constraints#
####################################################################
#
##
def Sys(model):
   
    # NODE
    
    # buying 'make up' power
    
    jan_node_cost = sum(model.jan_short[j,i]*model.RT_node[j*24+i] for j in model.jan_days for i in model.h)
    feb_node_cost = sum(model.feb_short[j,i]*model.RT_node[j*24+i] for j in model.feb_days for i in model.h)
    mar_node_cost = sum(model.mar_short[j,i]*model.RT_node[j*24+i] for j in model.mar_days for i in model.h)
    apr_node_cost = sum(model.apr_short[j,i]*model.RT_node[j*24+i] for j in model.apr_days for i in model.h)
    may_node_cost = sum(model.may_short[j,i]*model.RT_node[j*24+i] for j in model.may_days for i in model.h)
    jun_node_cost = sum(model.jun_short[j,i]*model.RT_node[j*24+i] for j in model.jun_days for i in model.h)
    jul_node_cost = sum(model.jul_short[j,i]*model.RT_node[j*24+i] for j in model.jul_days for i in model.h)
    aug_node_cost = sum(model.aug_short[j,i]*model.RT_node[j*24+i] for j in model.aug_days for i in model.h)
    sep_node_cost = sum(model.sep_short[j,i]*model.RT_node[j*24+i] for j in model.sep_days for i in model.h)
    oct_node_cost = sum(model.oct_short[j,i]*model.RT_node[j*24+i] for j in model.oct_days for i in model.h)
    nov_node_cost = sum(model.nov_short[j,i]*model.RT_node[j*24+i] for j in model.nov_days for i in model.h)
    dec_node_cost = sum(model.dec_short[j,i]*model.RT_node[j*24+i] for j in model.dec_days for i in model.h)

    # selling electricity at the node
    node_revenues = sum(model.WindDispatch[i]*model.RT_node[i] for i in model.Hours)

    # HUB
    
#    # wind developer pays insurer
    jan_hub_cost = sum(model.jan[i]*model.jan_contract_charge[j,i] for j in model.jan_days for i in model.h)
    feb_hub_cost = sum(model.feb[i]*model.feb_contract_charge[j,i] for j in model.feb_days for i in model.h)
    mar_hub_cost = sum(model.mar[i]*model.mar_contract_charge[j,i] for j in model.mar_days for i in model.h)
    apr_hub_cost = sum(model.apr[i]*model.apr_contract_charge[j,i] for j in model.apr_days for i in model.h)
    may_hub_cost = sum(model.may[i]*model.may_contract_charge[j,i] for j in model.may_days for i in model.h)
    jun_hub_cost = sum(model.jun[i]*model.jun_contract_charge[j,i] for j in model.jun_days for i in model.h)
    jul_hub_cost = sum(model.jul[i]*model.jul_contract_charge[j,i] for j in model.jul_days for i in model.h)
    aug_hub_cost = sum(model.aug[i]*model.aug_contract_charge[j,i] for j in model.aug_days for i in model.h)
    sep_hub_cost = sum(model.sep[i]*model.sep_contract_charge[j,i] for j in model.sep_days for i in model.h)
    oct_hub_cost = sum(model.oct[i]*model.oct_contract_charge[j,i] for j in model.oct_days for i in model.h)
    nov_hub_cost = sum(model.nov[i]*model.nov_contract_charge[j,i] for j in model.nov_days for i in model.h)
    dec_hub_cost = sum(model.dec[i]*model.dec_contract_charge[j,i] for j in model.dec_days for i in model.h)
   
#    # insurer pays wind developer
    jan_hub_rev = sum(model.jan[i]*model.jan_contract_payout[j,i] for j in model.jan_days for i in model.h)
    feb_hub_rev = sum(model.feb[i]*model.feb_contract_payout[j,i] for j in model.feb_days for i in model.h)
    mar_hub_rev = sum(model.mar[i]*model.mar_contract_payout[j,i] for j in model.mar_days for i in model.h)
    apr_hub_rev = sum(model.apr[i]*model.apr_contract_payout[j,i] for j in model.apr_days for i in model.h)
    may_hub_rev = sum(model.may[i]*model.may_contract_payout[j,i] for j in model.may_days for i in model.h)
    jun_hub_rev = sum(model.jun[i]*model.jun_contract_payout[j,i] for j in model.jun_days for i in model.h)
    jul_hub_rev = sum(model.jul[i]*model.jul_contract_payout[j,i] for j in model.jul_days for i in model.h)
    aug_hub_rev = sum(model.aug[i]*model.aug_contract_payout[j,i] for j in model.aug_days for i in model.h)
    sep_hub_rev = sum(model.sep[i]*model.sep_contract_payout[j,i] for j in model.sep_days for i in model.h)
    oct_hub_rev = sum(model.oct[i]*model.oct_contract_payout[j,i] for j in model.oct_days for i in model.h)
    nov_hub_rev = sum(model.nov[i]*model.nov_contract_payout[j,i] for j in model.nov_days for i in model.h)
    dec_hub_rev = sum(model.dec[i]*model.dec_contract_payout[j,i] for j in model.dec_days for i in model.h)
   
    return jan_node_cost + feb_node_cost + mar_node_cost + apr_node_cost + may_node_cost + jun_node_cost + jul_node_cost + aug_node_cost + sep_node_cost + oct_node_cost + nov_node_cost + dec_node_cost - node_revenues + jan_hub_cost + feb_hub_cost + mar_hub_cost + apr_hub_cost + may_hub_cost + jun_hub_cost + jul_hub_cost + aug_hub_cost + sep_hub_cost + oct_hub_cost + nov_hub_cost + dec_hub_cost - jan_hub_rev - feb_hub_rev - mar_hub_rev - apr_hub_rev - may_hub_rev - jun_hub_rev - jul_hub_rev - aug_hub_rev - sep_hub_rev - oct_hub_rev - nov_hub_rev - dec_hub_rev 

model.System = Objective(rule=Sys, sense=minimize)


# Constraints

# Wind Dispatch -- allows for curtailment during negative price events
def WindDis(model,i):
    return model.WindDispatch[i] <= model.Wind[i]
model.WindCon = Constraint(model.Hours,rule=WindDis)


##################################################################
# Only buy make up power when production is under target
##################################################################

def jan_short(model,i,j): 
    return model.jan_short[j,i] >= model.jan[i]-model.Wind[j*24+i]
model.shortjan = Constraint(model.h,model.jan_days,rule=jan_short)

def feb_short(model,i,j):    
    return model.feb_short[j,i] >= model.feb[i]-model.Wind[j*24+i]
model.shortfeb = Constraint(model.h,model.feb_days,rule=feb_short)

def mar_short(model,i,j):    
    return model.mar_short[j,i] >= model.mar[i]-model.Wind[j*24+i]
model.shortmar = Constraint(model.h,model.mar_days,rule=mar_short)

def apr_short(model,i,j):    
    return model.apr_short[j,i] >= model.apr[i]-model.Wind[j*24+i]
model.shortapr = Constraint(model.h,model.apr_days,rule=apr_short)

def may_short(model,i,j):    
    return model.may_short[j,i] >= model.may[i]-model.Wind[j*24+i]
model.shortmay = Constraint(model.h,model.may_days,rule=may_short)

def jun_short(model,i,j):    
    return model.jun_short[j,i] >= model.jun[i]-model.Wind[j*24+i]
model.shortjun = Constraint(model.h,model.jun_days,rule=jun_short)

def jul_short(model,i,j):    
    return model.jul_short[j,i] >= model.jul[i]-model.Wind[j*24+i]
model.shortjul = Constraint(model.h,model.jul_days,rule=jul_short)

def aug_short(model,i,j):    
    return model.aug_short[j,i] >= model.aug[i]-model.Wind[j*24+i]
model.shortaug = Constraint(model.h,model.aug_days,rule=aug_short)

def sep_short(model,i,j):    
    return model.sep_short[j,i] >= model.sep[i]-model.Wind[j*24+i]
model.shortsep = Constraint(model.h,model.sep_days,rule=sep_short)

def oct_short(model,i,j):    
    return model.oct_short[j,i] >= model.oct[i]-model.Wind[j*24+i]
model.shortoct = Constraint(model.h,model.oct_days,rule=oct_short)

def nov_short(model,i,j):    
    return model.nov_short[j,i] >= model.nov[i]-model.Wind[j*24+i]
model.shortnov = Constraint(model.h,model.nov_days,rule=nov_short)

def dec_short(model,i,j):    
    return model.dec_short[j,i] >= model.dec[i]-model.Wind[j*24+i]
model.shortdec = Constraint(model.h,model.dec_days,rule=dec_short)
    

##################################################################
# Only pay insurer when price is above strike 
##################################################################

def jan_charge(model,i,j): 
    return model.jan_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargejan = Constraint(model.h,model.jan_days,rule=jan_charge)

def feb_charge(model,i,j): 
    return model.feb_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargefeb = Constraint(model.h,model.feb_days,rule=feb_charge)

def mar_charge(model,i,j): 
    return model.mar_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargemar = Constraint(model.h,model.mar_days,rule=mar_charge)

def apr_charge(model,i,j): 
    return model.apr_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargeapr = Constraint(model.h,model.apr_days,rule=apr_charge)

def may_charge(model,i,j): 
    return model.may_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargemay = Constraint(model.h,model.may_days,rule=may_charge)

def jun_charge(model,i,j): 
    return model.jun_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargejun = Constraint(model.h,model.jun_days,rule=jun_charge)

def jul_charge(model,i,j): 
    return model.jul_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargejul = Constraint(model.h,model.jul_days,rule=jul_charge)

def aug_charge(model,i,j): 
    return model.aug_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargeaug = Constraint(model.h,model.aug_days,rule=aug_charge)

def sep_charge(model,i,j): 
    return model.sep_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargesep = Constraint(model.h,model.sep_days,rule=sep_charge)

def oct_charge(model,i,j): 
    return model.oct_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargeoct = Constraint(model.h,model.oct_days,rule=oct_charge)

def nov_charge(model,i,j): 
    return model.nov_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargenov = Constraint(model.h,model.nov_days,rule=nov_charge)

def dec_charge(model,i,j): 
    return model.dec_contract_charge[j,i] >= model.RT_hub[j*24+i] - model.Strike
model.chargedec = Constraint(model.h,model.dec_days,rule=dec_charge)


##################################################################
# Insurer only pays wind producer when price is below strike
##################################################################

def jan_payout(model,i,j): 
    return model.jan_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutjan = Constraint(model.h,model.jan_days,rule=jan_payout)

def feb_payout(model,i,j): 
    return model.feb_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutfeb = Constraint(model.h,model.feb_days,rule=feb_payout)

def mar_payout(model,i,j): 
    return model.mar_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutmar = Constraint(model.h,model.mar_days,rule=mar_payout)

def apr_payout(model,i,j): 
    return model.apr_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutapr = Constraint(model.h,model.apr_days,rule=apr_payout)

def may_payout(model,i,j): 
    return model.may_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutmay = Constraint(model.h,model.may_days,rule=may_payout)

def jun_payout(model,i,j): 
    return model.jun_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutjun = Constraint(model.h,model.jun_days,rule=jun_payout)

def jul_payout(model,i,j): 
    return model.jul_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutjul = Constraint(model.h,model.jul_days,rule=jul_payout)

def aug_payout(model,i,j): 
    return model.aug_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutaug = Constraint(model.h,model.aug_days,rule=aug_payout)

def sep_payout(model,i,j): 
    return model.sep_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutsep = Constraint(model.h,model.sep_days,rule=sep_payout)

def oct_payout(model,i,j): 
    return model.oct_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutoct = Constraint(model.h,model.oct_days,rule=oct_payout)

def nov_payout(model,i,j): 
    return model.nov_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutnov = Constraint(model.h,model.nov_days,rule=nov_payout)

def dec_payout(model,i,j): 
    return model.dec_contract_payout[j,i] <= model.Strike - model.RT_hub[j*24+i]
model.payoutdec = Constraint(model.h,model.dec_days,rule=dec_payout)


##################################################################
# Constrain hedge targets to align with P99 amounts
##################################################################

def Jan_Targets(model,i):  
    total = sum(model.jan[i] for i in model.h)
    return total == 2103
model.JanConstraint= Constraint(model.h, rule=Jan_Targets)

def feb_Targets(model,i):    
    total = sum(model.feb[i] for i in model.h)
    return total == 1961
model.FebConstraint= Constraint(model.h, rule=feb_Targets)

def mar_Targets(model,i):    
    total = sum(model.mar[i] for i in model.h)
    return total == 2360
model.marConstraint= Constraint(model.h, rule=mar_Targets)

def apr_Targets(model,i):    
    total = sum(model.apr[i] for i in model.h)
    return total == 2347
model.aprConstraint= Constraint(model.h, rule=apr_Targets)

def may_Targets(model,i):    
    total = sum(model.may[i] for i in model.h)
    return total == 2125
model.mayConstraint= Constraint(model.h, rule=may_Targets)

def jun_Targets(model,i):    
    total = sum(model.jun[i] for i in model.h)
    return total == 2200
model.junConstraint= Constraint(model.h, rule=jun_Targets)

def july_Targets(model,i):    
    total = sum(model.jul[i] for i in model.h)
    return total == 1829
model.julyConstraint= Constraint(model.h, rule=july_Targets)

def aug_Targets(model,i):    
    total = sum(model.aug[i] for i in model.h)
    return total == 1641
model.augConstraint= Constraint(model.h, rule=aug_Targets)

def sep_Targets(model,i):    
    total = sum(model.sep[i] for i in model.h)
    return total == 1978
model.sepConstraint= Constraint(model.h, rule=sep_Targets)

def oct_Targets(model,i):    
    total = sum(model.oct[i] for i in model.h)
    return total == 2152
model.octConstraint= Constraint(model.h, rule=oct_Targets)

def nov_Targets(model,i):    
    total = sum(model.nov[i] for i in model.h)
    return total == 2231
model.novConstraint= Constraint(model.h, rule=nov_Targets)

def dec_Targets(model,i):    
    total = sum(model.dec[i] for i in model.h)
    return total == 2111
model.decConstraint= Constraint(model.h, rule=dec_Targets)

############################################################
#### Battery section                                       #
############################################################
#
#model.MW = Param(within=PositiveIntegers)
#model.MWh = Param(within=PositiveIntegers)
#
############################################################
#### Decision variables                                    #
############################################################
#
###Amount of day-ahead energy generated by each thermal unit's 3 segments at each hour
#model.discharge = Var(model.Hours, within=NonNegativeReals)
#model.charge = Var(model.Hours, within=NonNegativeReals)
#model.discharge_on = Var(model.Hours, within=Binary)
#model.charge_on = Var(model.Hours, within=Binary)
#model.SOC  = Var(model.Hours, bounds=(0,model.MWh),initialize=0)
##
#####################################################################
###Objective function                                               #
#####################################################################
##
###
#def Profits(model):
#    revenues = sum(model.discharge[i]*model.RT_node[i] for i in model.Hours)
#    costs = sum(model.charge[i]*model.RT_node[i] for i in model.Hours) 
#    return costs - revenues
#model.SystemProfits = Objective(rule=Profits, sense=minimize)
#   
#####################################################################
##   Constraints                                                    #
#####################################################################
#   
##Discharge constraint
#def MW_cap1(model,i):
#    return model.discharge[i] <= model.MW*model.discharge_on[i]
#model.MW_cap1= Constraint(model.Hours,rule=MW_cap1)
#
##Discharge constraint
#def MW_cap2(model,i):
#    return model.discharge[i] <=  model.SOC[i]
#model.MW_cap2= Constraint(model.Hours,rule=MW_cap2)
#
##SOC constraint
#def SOC_cap1(model,i):
#    return model.SOC[i] <=  model.MWh
#model.SOC_cap1= Constraint(model.Hours,rule=SOC_cap1)
#
##SOC constraint
#def SOC_cap2(model,i):
#    if i == 0:
#        return model.SOC[i] == 0
#    else:
#        return model.SOC[i] == model.SOC[i-1] + 0.8*model.charge[i-1] - model.discharge[i-1]
#model.SOC_cap2= Constraint(model.Hours,rule=SOC_cap2)
#
##Charge constraint
#def Charge_1(model,i):
#    return model.charge[i] <=  model.MW*model.charge_on[i]
#model.charge1= Constraint(model.Hours,rule=Charge_1)
#
##Mode Constraint
#def Mode(model,i):
#    return model.discharge_on[i] + model.charge_on[i] <= 1
#model.ModeC= Constraint(model.Hours,rule=Mode)
#
