"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from platypus import NSGAII, Problem, Real 
import pandas as pd
import numpy as np
import time

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
        D = np.float(WP[i]*np.max([0,NP[i]]) - np.max([vars[(month-1)*2+p]-WP[i],0])*NP[i] + (strikeprice - HP[i])*vars[(month-1)*2+p])
        # DeveloperDaily = np.append(DeveloperDaily,D)
        DeveloperProfits += D
        
        T = np.float((HP[i] - strikeprice)*vars[(month-1)*2+p])
        TraderRevs += np.max([0,T])
        # TraderProfits += T
        
        DH = np.float((strikeprice - HP[i])*vars[(month-1)*2+p])
        DeveloperRevs += np.max([0,DH])
 
        # Monthly tracker
        if month != month_hold:
            month_hold = month
            Monthly.append(DeveloperMonth)
            DeveloperMonth = D
        else:
            DeveloperMonth += D
    
        # Constraints
        # offpeak = 0
        # peak = 0
        # for i in range(0,24,2):
        #     offpeak += vars[i]
        # for i in range(1,25,2):
        #     peak += vars[i]           
           
    # Hedge Volume Constraint
    # Constraints.append(8*offpeak + 16*peak - volume*1.03) 
    # Constraints.append(volume*0.97 - 8*offpeak - 16*peak) 
    
    Ratio = np.float(TraderRevs/DeveloperRevs)
    # DeveloperHedge = np.float(DeveloperHedge)
    for i in range(0,len(Monthly)-1):
        MonthlyVar += np.abs(Monthly[i] - Monthly[i+1])
    MonthlyVar = -MonthlyVar
    
    S = np.sort(Monthly)
    VAR = -sum(S[0:4])
    
    Constraints.append(Ratio - 1.12)
    Constraints.append(1.08 - Ratio)    
    Constraints = list(Constraints)
    
    return [DeveloperProfits, VAR], Constraints


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
algorithm.run(25000)

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)


#####################################################################
##########           OUTPUTS                 ########################
#####################################################################

# limit evalutaion to 'feasible' solutions
feasible_solutions = [s for s in algorithm.result if s.feasible]
 
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
    
# # # plot status quo
# ax.scatter(x/1000,y,-z,c='blue',s=36)
# ax.set_xlabel("Developer Profits ($1000s)")
# ax.set_ylabel("Ratio")
# ax.set_zlabel("Monthly Variability")

# plt.show()

df_D = pd.DataFrame(D)
df_D.to_csv('Decision_Variables.csv')

df_O = pd.DataFrame(O)
df_O.to_csv('Objective_Functions.csv')


