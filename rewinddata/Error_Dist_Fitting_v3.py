# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 21:55:04 2019

@author: kakdemi
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#creating empty dictionaries to keep hub height specific lists
daily_mean_speed_dict = {}
generated_daily_mean_dict = {}
predicted_daily_mean_dict = {}
wind_speed_error_dict = {}
predicted_daily_final_dict = {}
generated_error_dict = {}
#defining roughness length in meters
z0 = 0.03

#reading the csv file in which all the daily mean wind speeds are stored
Site_Daily_Mean_Speed = pd.read_csv("DailyMeanSpeed.csv", index_col="Date&Time", parse_dates=True)

#creating new columns in the dataframe to calculate alfa values for different hub heights
Site_Daily_Mean_Speed["Result_60"] = np.log(Site_Daily_Mean_Speed["60"]/Site_Daily_Mean_Speed["53"])
Site_Daily_Mean_Speed["Result_80"] = np.log(Site_Daily_Mean_Speed["80"]/Site_Daily_Mean_Speed["53"])
Site_Daily_Mean_Speed["Result_90"] = np.log(Site_Daily_Mean_Speed["90"]/Site_Daily_Mean_Speed["53"])
Site_Daily_Mean_Speed["Result_100"] = np.log(Site_Daily_Mean_Speed["100"]/Site_Daily_Mean_Speed["53"])
Site_Daily_Mean_Speed["Result_110"] = np.log(Site_Daily_Mean_Speed["110"]/Site_Daily_Mean_Speed["53"])
Site_Daily_Mean_Speed["Result_120"] = np.log(Site_Daily_Mean_Speed["120"]/Site_Daily_Mean_Speed["53"])
Site_Daily_Mean_Speed["Result_140"] = np.log(Site_Daily_Mean_Speed["140"]/Site_Daily_Mean_Speed["53"])
Site_Daily_Mean_Speed["Result_160"] = np.log(Site_Daily_Mean_Speed["160"]/Site_Daily_Mean_Speed["53"])
Site_Daily_Mean_Speed["Result_180"] = np.log(Site_Daily_Mean_Speed["180"]/Site_Daily_Mean_Speed["53"])
Site_Daily_Mean_Speed["Result_200"] = np.log(Site_Daily_Mean_Speed["200"]/Site_Daily_Mean_Speed["53"])

#creating an empty list to summarize alfa values for one average year
Day_Alfa = []

#finding alfa values for a normal average year of 365 days by taking the mean of same days in different years
for row in range(Site_Daily_Mean_Speed.shape[0]):
    Day_Alfa.append(str(Site_Daily_Mean_Speed.index[row])[5:10])

Site_Daily_Mean_Speed['Day'] = Day_Alfa

#taking the average of each day over all years represented
Average_Year = Site_Daily_Mean_Speed.groupby(['Day']).mean()

#reindexing the dataframe
New_Index = [str(value) for value in list(Average_Year.index)]
Average_Year["New_Index"] = New_Index
Average_Year.set_index("New_Index")

#dropping unused column
del Average_Year['New_Index']

#creating values for February 29 by taking the same values from February 28
Average_Year.loc["02-29"] = Average_Year.loc["02-28"]

#sorting dataframe by index
Average_Year = Average_Year.sort_index()

#defining the name of NOAA station
file = "NantucketDailyMeanSpeedHistorical.csv"
#reading date and daily wind speed data from csv file, and declaring index as dates
station_data = pd.read_csv(file, low_memory=False, parse_dates=True, index_col="Date&Time")
#declaring data type in wind speed column as numeric floats
station_data["Wind Speed"] = pd.to_numeric(station_data["Wind Speed"], errors='coerce')
#slicing data by dates
daily_station_data = station_data.loc["2016-12-01":"2018-12-31"].copy()
#changing the wind speed units from MPH to m/s
daily_station_data.loc[:,'Wind Speed'] *= 0.44704
#saving daily wind speeds in a list
daily_noaa_station_data = list(daily_station_data['Wind Speed'])
#calculating Hellmann exponent according to Spera and Richards (this is used to calculate 53 m wind speeds from 13.7 m wind speeds)
alfa = [((z0/13.7)**0.2)*(1-(0.55*np.log(v))) for v in daily_noaa_station_data]

for height in turbine_height:
    #creating the empty lists for every hub height in the dictionary
    daily_mean_speed_dict['daily_mean_speed_%s' % height] = []
    generated_daily_mean_dict['generated_daily_mean_%s' % height] = []
    predicted_daily_mean_dict['predicted_daily_mean_%s' % height] = []
    wind_speed_error_dict['error_%s' % height] = []
    predicted_daily_final_dict['predicted_daily_final_%s' % height] = []
    generated_error_dict['generated_error_%s' % height] = []
    
    #selecting speed data for each hub height and saving them in a list
    Hub_Daily_Mean_Speed = list(Site_Daily_Mean_Speed[str(height)]) 
    
    #adding the data to the hub height specific lists in dictionaries
    daily_mean_speed_dict['daily_mean_speed_'+str(height)].extend(Hub_Daily_Mean_Speed)

for a in list(range(0,761)):
    #calculating 53 m wind speeds by using 13.7 m wind speeds
    generated_daily_values_53 = [daily_noaa_station_data[a] * ((53/13.7)**alfa[a])]
    #adding the data to the hub height specific lists in dictionary
    generated_daily_mean_dict['generated_daily_mean_53'].extend(generated_daily_values_53)

#creating a dataframe which stores generated daily mean wind speeds at 53 m
list_labels = ["Date&Time", "Wind53"]
list_columns = [list(Site_Daily_Mean_Speed.index), generated_daily_mean_dict['generated_daily_mean_53']]
zipped_list = list(zip(list_labels, list_columns))
wind_dict = dict(zipped_list)
Power_Law_53 = pd.DataFrame(wind_dict)
#declaring the index of the dataframe as date column
Power_Law_53 = Power_Law_53.set_index("Date&Time")

#to calculate wind speeds at other hub-heights, alfa is calculated by using the offshore data. Therefore, hub heights excluding 53 m are listed. 
new_height = [60, 80, 90, 100, 110, 120, 140, 160, 180, 200]

#creating dictionaries which stores days in months, and month order
day_dict = {'January':31, 'February':28, 'March':31, 'April':30, 'May':31, 'June':30, 'July':31, 'August':31, 'September':30, 'October':31, 'November':30, 'December':31}
month_dict = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}

#defining the years
years = ['2016','2017','2018'] 

for year in years:
    
#including December 2016 data
    if year == '2016': 
        months = ['December']
    else:
        months = ['January', 'February','March','April','May','June','July','August','September','October','November','December']

    for month in months:
        #finding the day numbers for every month
        day_numbers = list(range(1,int(day_dict[month]+1)))
        day_numbers = pd.Series(day_numbers)
        day_numbers = day_numbers.apply(lambda x:'{:0>2}'.format(x))
        day_numbers = list(day_numbers)
        
        for new_h in new_height:
            
            for day_no in day_numbers:
                
                #calculating the new alfa
                new_alfa = float(Average_Year["Result_"+str(new_h)][str(month_dict[month])+'-'+str(day_no)]/(np.log(new_h/53)))
                #finding the new wind speeds at different hub heights by using the power law
                generated_speeds = [Power_Law_53["Wind53"][str(str(year)+'-'+str(month_dict[month])+'-'+str(day_no))] * ((new_h/53)**new_alfa)]
                #adding the data to the hub height specific lists in dictionary
                generated_daily_mean_dict['generated_daily_mean_'+str(new_h)].extend(generated_speeds)
            
for height in turbine_height:
    
    #changing the type of data as numpy array
    daily_mean_speed_array = np.asarray(daily_mean_speed_dict['daily_mean_speed_'+str(height)])
    noaa_station_daily_wind_array = np.asarray(generated_daily_mean_dict['generated_daily_mean_'+str(height)])
    #finding the statistical values of the linear regression
    slope, intercept, r_value, p_value, std_err = st.linregress(noaa_station_daily_wind_array, daily_mean_speed_array)
    #printing the R-Squared value
    print("R-Squared for Hub Height of "+str(height)+" m:", r_value**2)
    #calculating the correlation coefficient
    corr_coeff, pvalue = st.pearsonr(noaa_station_daily_wind_array, daily_mean_speed_array)
    #printing the correlation coefficient
    print("Pearson Correlation Coefficient for Hub Height of "+str(height)+" m:", corr_coeff)
    
    #predicting wind speeds at the project site by using the equation acquired from linear regression
    predicted_wind_at_site = [(b*slope)+intercept for b in generated_daily_mean_dict['generated_daily_mean_'+str(height)]]
    #adding the data to the hub height specific lists in dictionary
    predicted_daily_mean_dict['predicted_daily_mean_'+str(height)].extend(predicted_wind_at_site)
    #finding the difference between actual and predicted wind speeds at the project site
    predicted_vs_actual = [predict - actual for predict, actual in zip(predicted_daily_mean_dict['predicted_daily_mean_'+str(height)], daily_mean_speed_dict['daily_mean_speed_'+str(height)])]
    #adding error data to the hub height specific lists in dictionary
    wind_speed_error_dict['error_'+str(height)].extend(predicted_vs_actual)
    
# fit distribution to model errors

import warnings
import statsmodels as sm
import matplotlib

matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')

errors = pd.DataFrame(wind_speed_error_dict['error_53'])
data = errors

# Create models from data
def best_fit_distribution(data, bins=100, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
    DISTRIBUTIONS = [        
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
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
ax = data.plot(kind='hist', bins=50, density=True, alpha=0.5)
# Save plot limits
dataYLim = ax.get_ylim()

# Find best fit distribution
best_fit_name, best_fit_params = best_fit_distribution(data, 100, ax)
best_dist = getattr(st, best_fit_name)

# Update plots
ax.set_ylim(dataYLim)
ax.set_title(u'Error Histogram')
ax.set_xlabel(u'Error Between Predicted and Actual Wind Speeds at 53 m (m/s)')
ax.set_ylabel('Frequency')

# Make PDF with best params 
pdf = make_pdf(best_dist, best_fit_params)

# Display
plt.figure(figsize=(12,8))
ax = pdf.plot(lw=2, label='PDF', legend=True)
data.plot(kind='hist', bins=50, density=True, alpha=0.5, label='Data', legend=True, ax=ax)

param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
dist_str = '{}({})'.format(best_fit_name, param_str)

ax.set_title(u'Error Histogram')
ax.set_xlabel(u'Error Between Predicted and Actual Wind Speeds at 53 m (m/s)')
ax.set_ylabel('Frequency')
    
    