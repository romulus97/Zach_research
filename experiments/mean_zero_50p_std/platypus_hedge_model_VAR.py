"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from platypus import NSGAII, Problem, Real 
import pandas as pd
import numpy as np
import time
import no_hedge

start = time.time()

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import constant inputs
df_data = pd.read_csv('input_data.csv', header=0)
X = df_data.values
HubPrices = X[:,0]
NodePrices = X[:,1]
WindPower = X[:,2]

# Calendar lookup
calendar = pd.read_csv('calendar.csv',header=0)
a = range(24)
b = np.tile(a,365)
calendar['Hours'] = b
years = int(len(HubPrices)/8760)
C = calendar.values

strikeprice = 22.64

floor_months = 10

#####################################################################
##########              BASIS RISK SCENARIO        ########################
#####################################################################


BasisRisk = NodePrices - HubPrices

bias = np.mean(BasisRisk)
spread = np.std(BasisRisk)

# Alter nodal prices
BasisRisk = (BasisRisk - bias)/(spread*(1-.50))
NodePrices = HubPrices + BasisRisk

#####################################################################
##########         Performance Measures        ######################
#####################################################################

# Defined maximum (no hedge) revenues
N = no_hedge.sim(HubPrices,NodePrices,WindPower,C,floor_months)
max_rev = N[0]
sorted_monthly = np.sort(N[2])
floor = sum(sorted_monthly[0:floor_months])


#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################

# simulation model
def simulate(vars, 
             strikeprice = strikeprice,
             HP = HubPrices,
             NP = NodePrices,
             WP = WindPower,
             calendar=C,
             RX = max_rev,
             V = floor
             ):
    
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
        D = float(WP[i]*max([0,NP[i]]) - max([vars[(month-1)*2+p]-WP[i],0])*NP[i] + (strikeprice - HP[i])*vars[(month-1)*2+p])
        # DeveloperDaily = np.append(DeveloperDaily,D)
        DeveloperProfits += D
        
        T = float((HP[i] - strikeprice)*vars[(month-1)*2+p])
        TraderRevs += max([0,T])
        # TraderProfits += T
        
        DH = float((strikeprice - HP[i])*vars[(month-1)*2+p])
        DeveloperRevs += max([0,DH])
 
        # Monthly tracker
        if month != month_hold:
            month_hold = month
            Monthly.append(DeveloperMonth)
            
            if len(Monthly) <= 10:
                mins.append(DeveloperMonth)
            else:
                M = max(mins)
                if M > DeveloperMonth:
                    idx = mins.index(M)
                    mins[idx] = DeveloperMonth
            
            DeveloperMonth = D
                        
        else:
            DeveloperMonth += D

    
    Ratio = float(TraderRevs/DeveloperRevs)
    # DeveloperHedge = np.float(DeveloperHedge)
    for i in range(0,len(Monthly)-1):
        MonthlyVar += abs(Monthly[i] - Monthly[i+1])
    MonthlyVar = -MonthlyVar
    
    VAR = sum(mins)
    Floor_improvement = VAR - V
    
    Constraints.append(Ratio - 1.12)
    Constraints.append(1.08 - Ratio)    
    Constraints = list(Constraints)
    
    Profit_fraction = float(DeveloperProfits/RX)
    
    return [Profit_fraction, Floor_improvement], Constraints


#####################################################################
##########           MOEA EXECUTION          ########################
#####################################################################

# Define Platypus problem
no_vars = 24
no_objs = 2
no_constraints = 2
problem = Problem(no_vars,no_objs,no_constraints)
problem.types[:] = Real(0,200)
problem.constraints[:] = "<=0"
problem.directions[:] = Problem.MAXIMIZE
problem.function = simulate
algorithm = NSGAII(problem)

# Evaluate function # of times
algorithm.run(35000)

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)


#####################################################################
##########           OUTPUTS                 ########################
#####################################################################

# limit evalutaion to 'feasible' solutions
feasible_solutions = [s for s in algorithm.result if s.feasible]

D = np.zeros((len(feasible_solutions),no_vars))
O = np.zeros((len(feasible_solutions),no_objs))

for s in feasible_solutions:
    
    idx = feasible_solutions.index(s)
    # ax.scatter(s.objectives[0]/1000,s.objectives[1],s.objectives[2]*-1, c = 'red',alpha=0.5)

    #record solution information
    for i in range(0,no_vars):
        D[idx,i] = s.variables[i]
    for j in range(0,no_objs):
        O[idx,j] = s.objectives[j]

df_D = pd.DataFrame(D)
df_D.to_csv('Decision_Variables.csv')

df_O = pd.DataFrame(O)
df_O.to_csv('Objective_Functions.csv')
    
# display the tradeoff frontier   
# from mpl_toolkits.mplot3d import Axes3D 
# import matplotlib.pyplot as plt

# plot status quo solution
# import hedge_sim
# strikeprice = 22.64
# df_H = pd.read_excel('P50.xlsx',sheet_name = 'hedge_targets',header=None)
# hedgetargets = df_H.values
# x,y,z = hedge_sim.simulate(hedgetargets,strikeprice,HubPrices,NodePrices,WindPower,C)
# print(y)

# # 2 objective results
# plt.scatter([s.objectives[0]/1000 for s in feasible_solutions],
#             [s.objectives[1] for s in feasible_solutions],c='red',alpha=0.5)

# # plot status quo
# plt.scatter(x/1000,y,c='blue',s=36)

# plt.xlabel("Developer Profits ($1000s)")
# plt.ylabel("Ratio")
# plt.show()


# 3 objective results
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

    
# # # plot status quo
# ax.scatter(x/1000,y,-z,c='blue',s=36)
# ax.set_xlabel("Developer Profits ($1000s)")
# ax.set_ylabel("Ratio")
# ax.set_zlabel("Monthly Variability")

# plt.show()




