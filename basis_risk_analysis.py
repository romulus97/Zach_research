# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:00:54 2019

@author: jkern
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from sklearn import linear_model

# read in excel file with price data
df_prices = pd.read_excel('SPP_LMPs.xlsx',sheet_name='Historical LMP',header=1)

# selecting only real time nodal prices for 2015
rtn2015 = df_prices['RT_NODE_2015']

# exclude the NAN values
rtn2015_edit = rtn2015.iloc[:8760]

# selecting only real time nodal prices for 2016
rtn2016 = df_prices['RT_NODE_2016']

# append 2015 and 2016 prices
rtn_both = rtn2015_edit.append(rtn2016)

# convert to numerical array
RTN = np.array(rtn_both)

#plot 2015 and 2016 nodal prices
plt.plot(RTN)
plt.xlabel('Hour')
plt.ylabel('Price $/MWh')
plt.show()

#now do the same thing with hub prices

# selecting only real time hub prices for 2015
rth2015 = df_prices['RT_HUB_2015']

# exclude the NAN values
rth2015_edit = rth2015.iloc[:8760]

# selecting only real time hub prices for 2016
rth2016 = df_prices['RT_HUB_2016']

# append 2015 and 2016 prices
rth_both = rth2015_edit.append(rth2016)

# convert to numerical array
RTH = np.array(rth_both)

#plot 2015 and 2016 hub prices
plt.plot(RTH,color='r')
plt.xlabel('Hour')
plt.ylabel('Price $/MWh')
plt.show()

########################################################################

#now read in wind speed data

# read in excel file with wind speed data
df_wind = pd.read_excel('SPP_wind data_20180309.xlsx',sheet_name='Historical 8760s',header=14)

# selecting only wind power for 2015
wind2015 = df_wind['2015_MWh']

# exclude the NAN values
wind2015_edit = wind2015.iloc[:8760]

# selecting only wind power for 2016
wind2016 = df_wind['2016_MWh']

# append 2015 and 2016 wind power
wind_both = wind2015_edit.append(wind2016)

# convert to numerical array
WIND = np.array(wind_both)

#plot 2015 and 2016 hub prices
plt.plot(WIND,color='g')
plt.xlabel('Hour')
plt.ylabel('Energy (MWh')
plt.show()

#########################################################################

# difference between hub price and node price
basis_difference = RTH - RTN

#scatter plot of wind (x axis) and basis risk (y axis)
plt.scatter(WIND,basis_difference,c='orange',alpha=0.5,edgecolors='black')
plt.xlabel('Wind (MWh)')
plt.ylabel('Hub minus Node ($/MWh)')

# combine wind and basis risk data into a single array
combined = np.column_stack((WIND,basis_difference))

# convert single array to pandas dataframe and rename columns
df_combined = pd.DataFrame(combined)
df_combined.columns = ['Wind','Basis_Risk']

# drop NaN values from dataframe
cleaned = df_combined.dropna()

# calculate pearson R correlation
r = st.pearsonr(cleaned['Wind'],cleaned['Basis_Risk'])
print('The correlation and p-value are ' + str(r))


#########################################################################

#read in electricity demand data

# set counter equal to 0
counter = 0

# iterate over two years
for year in range(2015,2017):
    
    # iterate over 12 months    
    for i in range(1,13):
            
        #base of filename
        base = 'HOURLY_LOAD-' + str(year)
        
        if i < 10:
            adder = '0' + str(i)
        else:
            adder = str(i)
        
        #specify filename to read
        filename = base + adder + '.csv'
        
        #read data 
        data = pd.read_csv(filename,header=0)
  
        # if it's the first month we're reading in, set demand = data
        if counter < 1:
             
            demand = data
        
        # otherwise, stack new data underneath old data
        else:
            
            demand = pd.concat((demand,data),sort=False)
        
        counter = counter + 1
    
#get rid of duplicate values
shortened = demand.drop_duplicates()

#reset index
S = shortened.reset_index(drop=True)

#calculate total SPP demand
SPP_total =[]
for i in range(0,len(S)):
    total = np.sum(S.loc[i,' CSWS':' WR'])
    if total >0:
        SPP_total.append(total)
        
#plot SPP electricity demand
plt.figure()
plt.plot(SPP_total,color='b')
plt.xlabel('Hour')
plt.ylabel('Demand (MWh')
plt.show()


#scatter plot of wind (x axis) and basis risk (y axis)
plt.scatter(SPP_total,basis_difference,c='blue',alpha=0.3,edgecolors='black')
plt.xlabel('Demand(MWh)')
plt.ylabel('Hub minus Node ($/MWh)')

# combine wind and basis risk data into a single array
combined = np.column_stack((SPP_total,basis_difference))

# convert single array to pandas dataframe and rename columns
df_combined = pd.DataFrame(combined)
df_combined.columns = ['Demand','Basis_Risk']

# drop any NaN values from dataframe
cleaned2 = df_combined.dropna()

# calculate pearson R correlation
r = st.pearsonr(cleaned2['Demand'],cleaned2['Basis_Risk'])
print('The correlation and p-value are ' + str(r))

#############################################
# multivariate regresssion of wind production, demand, and basis risk

# combine wind and basis risk data into a single array
combined = np.column_stack((WIND,SPP_total,basis_difference))
df_combined = pd.DataFrame(combined)
df_combined.columns = ['Wind','Demand','Basis_Risk']
cleaned = df_combined.dropna()

# define linear regression object
reg = linear_model.LinearRegression()

# Train the models using a training set
X = np.column_stack((cleaned['Wind'],cleaned['Demand']))
reg.fit(X,cleaned['Basis_Risk'])

# print intercept
print(reg.intercept_)

# print coefficients
print(reg.coef_)

# regression equation
# y = coef#1 * wind + coef#2 * demand + intercept

W = cleaned.loc[:,'Wind']
D = cleaned.loc[:,'Demand']
B = cleaned.loc[:,'Basis_Risk']

# estimating basis risk as a function of wind and demand
Y = []
for i in range(0,len(W)):
    
    y_hat = reg.coef_[0]*W.iloc[i] + reg.coef_[1]*D.iloc[i] + reg.intercept_
    
    Y.append(y_hat)
    
# compare estimated and actual basis risk
plt.figure()
plt.plot(B,'b')
plt.plot(Y,'r')
plt.ylabel('Basis Risk ($/MWh)')
plt.xlabel('Frequency')

# error analysis 
errors = Y - B
plt.figure()
plt.hist(errors,50)
plt.xlabel('Error ($/MWh)')
plt.ylabel('Frequency')

# model basis risk as function of fitted regression + synthetic errors sampled
# from fitted distribution

# fit distribution to model errors

import warnings
import numpy as np
import pandas as pd
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')

data = errors

# Create models from data
def best_fit_distribution(data, bins=100, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
    DISTRIBUTIONS = [        
        st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
    ]

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    end
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params)

def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf

## Load data from statsmodels datasets
#data = pd.Series(sm.datasets.elnino.load_pandas().data.set_index('YEAR').values.ravel())
#
# Plot for comparison
plt.figure(figsize=(12,8))
ax = data.plot(kind='hist', bins=50, normed=True, alpha=0.5)
# Save plot limits
dataYLim = ax.get_ylim()

# Find best fit distribution
best_fit_name, best_fit_params = best_fit_distribution(data, 100, ax)
best_dist = getattr(st, best_fit_name)

# Update plots
ax.set_ylim(dataYLim)
ax.set_title(u'Basis Risk Prediction Errors')
ax.set_xlabel(u'Basis Risk($/MWh)')
ax.set_ylabel('Frequency')

# Make PDF with best params 
pdf = make_pdf(best_dist, best_fit_params)

# Display
plt.figure(figsize=(12,8))
ax = pdf.plot(lw=2, label='PDF', legend=True)
data.plot(kind='hist', bins=50, normed=True, alpha=0.5, label='Data', legend=True, ax=ax)

param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
dist_str = '{}({})'.format(best_fit_name, param_str)

ax.set_title(u'Basis Risk Prediction Errors')
ax.set_xlabel(u'Basis Risk($/MWh)')
ax.set_ylabel('Frequency')


# generate # of random samples from best fit distribution

empty = []
for i in range(0,len(errors)):
    e = st.cauchy.rvs(loc=best_fit_params[0], scale=best_fit_params[1], size=1)
    
    while e > 45 or e < -700:
        e = st.cauchy.rvs(loc=best_fit_params[0], scale=best_fit_params[1], size=1)
        
    empty.append(e)
    

plt.figure()
plt.hist(errors,alpha=0.5)
plt.hist(empty,alpha=0.5)


        
        
    