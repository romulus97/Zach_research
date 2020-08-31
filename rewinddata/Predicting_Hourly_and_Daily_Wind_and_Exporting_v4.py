# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 19:53:33 2020

@author: kakdemi
"""

import pandas as pd 
import numpy as np
from scipy import stats as st
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#defining different turbine heights
turbine_height = [53, 60, 80, 90, 100, 110, 120, 140, 160, 180, 200]
#creating empty dictionaries to keep hub height specific lists
daily_mean_speed_dict = {}
generated_daily_mean_dict = {}
predicted_daily_mean_dict = {}
wind_speed_error_dict = {}
predicted_daily_final_dict = {}
generated_error_dict = {}
regression_coeff_dict = {}
generated_all_data_dict = {}
predicted_all_data_dict = {}
all_random_errors_dict = {}
predicted_all_final_dict = {}
hourly_profiles_dict = {}
hourly_generated_dict = {}
hourly_site_dict = {}
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
    regression_coeff_dict['coeff_%s' % height] = []
    generated_all_data_dict['generated_daily_mean_%s' % height] = []
    predicted_all_data_dict['predicted_daily_mean_%s' % height] = []
    all_random_errors_dict['generated_error_%s' % height] = []
    predicted_all_final_dict['predicted_daily_final_%s' % height] = []
    hourly_profiles_dict['hourly_profile_%s' % height] = []
    hourly_generated_dict['predicted_hourly_final_%s' % height] = []
    hourly_site_dict['hourly_mean_speed_%s' % height] = []
    
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
    #adding regression coefficients to the hub height specific lists in dictionaries
    regression_coeff_dict['coeff_'+str(height)].extend([slope])
    regression_coeff_dict['coeff_'+str(height)].extend([intercept])
    
    #predicting wind speeds at the project site by using the equation acquired from linear regression
    predicted_wind_at_site = [(b*slope)+intercept for b in generated_daily_mean_dict['generated_daily_mean_'+str(height)]]
    #adding the data to the hub height specific lists in dictionary
    predicted_daily_mean_dict['predicted_daily_mean_'+str(height)].extend(predicted_wind_at_site)
    #finding the difference between actual and predicted wind speeds at the project site
    predicted_vs_actual = [predict - actual for predict, actual in zip(predicted_daily_mean_dict['predicted_daily_mean_'+str(height)], daily_mean_speed_dict['daily_mean_speed_'+str(height)])]
    #adding error data to the hub height specific lists in dictionary
    wind_speed_error_dict['error_'+str(height)].extend(predicted_vs_actual)
    
#generating random errors from best fitted distributions and by using the best parameters, and adding them to the hub height specific lists in dictionary
random_errors_53 = list(st.burr.rvs(92.65808166208735, 0.913523229166328, size=len(wind_speed_error_dict['error_53'])))
generated_error_dict['generated_error_53'].extend(random_errors_53)
random_errors_60 = list(st.weibull_min.rvs(5.918820885111755, size=len(wind_speed_error_dict['error_60'])))
generated_error_dict['generated_error_60'].extend(random_errors_60)
random_errors_80 = list(st.burr.rvs(20.667396420496882, 0.5698666725411307, size=len(wind_speed_error_dict['error_80'])))
generated_error_dict['generated_error_80'].extend(random_errors_80)
random_errors_90 = list(st.burr.rvs(6129.433767495797, 47276.40296572971, size=len(wind_speed_error_dict['error_90'])))
generated_error_dict['generated_error_90'].extend(random_errors_90)
random_errors_100 = list(st.burr.rvs(3011.021881557135, 37262.43825491163, size=len(wind_speed_error_dict['error_100'])))
generated_error_dict['generated_error_100'].extend(random_errors_100)
random_errors_110 = list(st.burr.rvs(19.654825138663654, 0.5048442611324359, size=len(wind_speed_error_dict['error_110'])))
generated_error_dict['generated_error_110'].extend(random_errors_110)
random_errors_120 = list(st.burr.rvs(3899.4184311025824, 18.59513421530066, size=len(wind_speed_error_dict['error_120'])))
generated_error_dict['generated_error_120'].extend(random_errors_120)
random_errors_140 = list(st.burr.rvs(30.92077226462459, 0.5766117218664566, size=len(wind_speed_error_dict['error_140'])))
generated_error_dict['generated_error_140'].extend(random_errors_140)
random_errors_160 = list(st.burr.rvs(15.821212030978682, 0.4076335982207494, size=len(wind_speed_error_dict['error_160'])))
generated_error_dict['generated_error_160'].extend(random_errors_160)
random_errors_180 = list(st.burr.rvs(16.856616009163133, 0.3882784926535954, size=len(wind_speed_error_dict['error_180'])))
generated_error_dict['generated_error_180'].extend(random_errors_180)
random_errors_200 = list(st.burr.rvs(98.26358840417907, 0.6218663843831695, size=len(wind_speed_error_dict['error_200'])))
generated_error_dict['generated_error_200'].extend(random_errors_200)
 
for height in turbine_height:
    #summing predicted wind speed from linear regression and generated error to find final prediction
    prediction_values = [predicted_daily_mean_dict['predicted_daily_mean_'+str(height)][t] + generated_error_dict['generated_error_'+str(height)][t] for t in range(len(predicted_daily_mean_dict['predicted_daily_mean_'+str(height)]))]
    #writing 0 where there are any negative values in predicted wind speeds
    new_prediction_values = [0 if p < 0 else p for p in prediction_values]
    #adding final predicted wind speeds to hub height specific lists in dictionary
    predicted_daily_final_dict['predicted_daily_final_'+str(height)].extend(new_prediction_values)
    
    #changing the type of data as numpy array
    daily_mean_speed_array = np.asarray(daily_mean_speed_dict['daily_mean_speed_'+str(height)])
    predicted_final_array = np.asarray(predicted_daily_final_dict['predicted_daily_final_'+str(height)])
    #finding the statistical values of the linear regression
    slope, intercept, r_value, p_value, std_err = st.linregress(predicted_final_array, daily_mean_speed_array)
    #printing the R-Squared value
    print("R-Squared (including error) for Hub Height of "+str(height)+" m:", r_value**2)
    #calculating the correlation coefficient
    corr_coeff, pvalue = st.pearsonr(predicted_final_array, daily_mean_speed_array)
    #printing the correlation coefficient
    print("Pearson Correlation Coefficient (including error) for Hub Height of "+str(height)+" m:", corr_coeff)
    
#defining the name of NOAA station
file = "NantucketDailyMeanSpeedHistorical.csv"
#reading date and daily wind speed data from csv file, and declaring index as dates
station_data = pd.read_csv(file, low_memory=False, parse_dates=True, index_col="Date&Time")
#declaring data type in wind speed column as numeric floats
station_data["Wind Speed"] = pd.to_numeric(station_data["Wind Speed"], errors='coerce')
#slicing data by dates
daily_station_data = station_data.loc["1948-01-01":"2016-11-30"].copy()
#changing the wind speed units from MPH to m/s
daily_station_data.loc[:,'Wind Speed'] *= 0.44704
#saving daily wind speeds in a list
daily_noaa_station_data = list(daily_station_data['Wind Speed'])
#to prevent natural logarithms to fail, 0 m/s wind speeds are transformed
daily_noaa_station_data = [0.00001 if p == 0 else p for p in daily_noaa_station_data]
#calculating Hellmann exponent according to Spera and Richards (this is used to calculate 53 m wind speeds from 13.7 m wind speeds)
alfa = [((z0/13.7)**0.2)*(1-(0.55*np.log(v))) for v in daily_noaa_station_data]

for a in list(range(daily_station_data.shape[0])):
    #calculating 53 m wind speeds by using 13.7 m wind speeds
    generated_daily_values_53 = [daily_noaa_station_data[a] * ((53/13.7)**alfa[a])]
    #adding the data to the hub height specific lists in dictionary
    generated_all_data_dict['generated_daily_mean_53'].extend(generated_daily_values_53)
    
#creating a dataframe which stores generated daily mean wind speeds at 53 m
list_labels = ["Date&Time", "Wind53"]
list_columns = [list(daily_station_data.index), generated_all_data_dict['generated_daily_mean_53']]
zipped_list = list(zip(list_labels, list_columns))
wind_dict = dict(zipped_list)
Power_Law_53 = pd.DataFrame(wind_dict)
#declaring the index of the dataframe as date column
Power_Law_53 = Power_Law_53.set_index("Date&Time")

#to calculate wind speeds at other hub-heights, alfa is calculated by using the offshore data. Therefore, hub heights excluding 53 m are listed. 
new_height = [60, 80, 90, 100, 110, 120, 140, 160, 180, 200]

#creating dictionaries which stores month order
month_dict = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}

#defining the years
years = [str(year_no) for year_no in range(1948,2017)]

for year in years:
    
    if int(year) % 4 == 0:
        day_dict= {'January':31, 'February':29, 'March':31, 'April':30, 'May':31, 'June':30, 'July':31, 'August':31, 'September':30, 'October':31, 'November':30, 'December':31}
    else:
        day_dict = {'January':31, 'February':28, 'March':31, 'April':30, 'May':31, 'June':30, 'July':31, 'August':31, 'September':30, 'October':31, 'November':30, 'December':31}
    if year == '2016': 
        months = ['January', 'February','March','April','May','June','July','August','September','October','November']
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
                generated_all_data_dict['generated_daily_mean_'+str(new_h)].extend(generated_speeds)
                
for height in turbine_height:
    
    #predicting wind speeds at the project site by using the equation acquired from linear regression
    predicted_wind_at_site = [(b*regression_coeff_dict['coeff_'+str(height)][0])+regression_coeff_dict['coeff_'+str(height)][1] for b in generated_all_data_dict['generated_daily_mean_'+str(height)]]
    #adding the data to the hub height specific lists in dictionary
    predicted_all_data_dict['predicted_daily_mean_'+str(height)].extend(predicted_wind_at_site)

#generating random errors from best fitted distributions and by using the best parameters, and adding them to the hub height specific lists in dictionary
random_errors_53 = list(st.burr.rvs(92.65808166208735, 0.913523229166328, size=len(range(daily_station_data.shape[0]))))            
all_random_errors_dict['generated_error_53'].extend(random_errors_53)
random_errors_60 = list(st.weibull_min.rvs(5.918820885111755, size=len(range(daily_station_data.shape[0]))))
all_random_errors_dict['generated_error_60'].extend(random_errors_60)
random_errors_80 = list(st.burr.rvs(20.667396420496882, 0.5698666725411307, size=len(range(daily_station_data.shape[0]))))
all_random_errors_dict['generated_error_80'].extend(random_errors_80)
random_errors_90 = list(st.burr.rvs(6129.433767495797, 47276.40296572971, size=len(range(daily_station_data.shape[0]))))
all_random_errors_dict['generated_error_90'].extend(random_errors_90)
random_errors_100 = list(st.burr.rvs(3011.021881557135, 37262.43825491163, size=len(range(daily_station_data.shape[0]))))
all_random_errors_dict['generated_error_100'].extend(random_errors_100)
random_errors_110 = list(st.burr.rvs(19.654825138663654, 0.5048442611324359, size=len(range(daily_station_data.shape[0]))))
all_random_errors_dict['generated_error_110'].extend(random_errors_110)
random_errors_120 = list(st.burr.rvs(3899.4184311025824, 18.59513421530066, size=len(range(daily_station_data.shape[0]))))
all_random_errors_dict['generated_error_120'].extend(random_errors_120)
random_errors_140 = list(st.burr.rvs(30.92077226462459, 0.5766117218664566, size=len(range(daily_station_data.shape[0]))))
all_random_errors_dict['generated_error_140'].extend(random_errors_140)
random_errors_160 = list(st.burr.rvs(15.821212030978682, 0.4076335982207494, size=len(range(daily_station_data.shape[0]))))
all_random_errors_dict['generated_error_160'].extend(random_errors_160)
random_errors_180 = list(st.burr.rvs(16.856616009163133, 0.3882784926535954, size=len(range(daily_station_data.shape[0]))))
all_random_errors_dict['generated_error_180'].extend(random_errors_180)
random_errors_200 = list(st.burr.rvs(98.26358840417907, 0.6218663843831695, size=len(range(daily_station_data.shape[0]))))
all_random_errors_dict['generated_error_200'].extend(random_errors_200)
 
for height in turbine_height:
    #summing predicted wind speed from linear regression and generated error to find final prediction
    prediction_values = [predicted_all_data_dict['predicted_daily_mean_'+str(height)][t] + all_random_errors_dict['generated_error_'+str(height)][t] for t in range(daily_station_data.shape[0])]
    #writing 0 where there are any negative values in predicted wind speeds
    new_prediction_values = [0 if p < 0 else p for p in prediction_values]
    #adding final predicted wind speeds to hub height specific lists in dictionary
    predicted_all_final_dict['predicted_daily_final_'+str(height)].extend(new_prediction_values)
    
#creating a dataframe for the complete daily mean dataset
list_labels = ["Date&Time", 53, 60, 80, 90, 100, 110, 120, 140, 160, 180, 200]
list_columns = [list(daily_station_data.index), predicted_all_final_dict['predicted_daily_final_53'], predicted_all_final_dict['predicted_daily_final_60'], 
                predicted_all_final_dict['predicted_daily_final_80'], predicted_all_final_dict['predicted_daily_final_90'], 
                predicted_all_final_dict['predicted_daily_final_100'], predicted_all_final_dict['predicted_daily_final_110'], 
                predicted_all_final_dict['predicted_daily_final_120'], predicted_all_final_dict['predicted_daily_final_140'], 
                predicted_all_final_dict['predicted_daily_final_160'], predicted_all_final_dict['predicted_daily_final_180'], 
                predicted_all_final_dict['predicted_daily_final_200']]
zipped_list = list(zip(list_labels, list_columns))
daily_wind_dict = dict(zipped_list)
Predicted_Daily_Mean_Speed = pd.DataFrame(daily_wind_dict)
#declaring the index of the dataframe as date column
Predicted_Daily_Mean_Speed = Predicted_Daily_Mean_Speed.set_index("Date&Time")

#reading the csv file that contains daily wind speeds at project site
Site_Daily_Wind_Speed = pd.read_csv("DailyMeanSpeed.csv", index_col="Date&Time", parse_dates=True)
#creating a dataframe for the daily mean dataset from project site
list_labels = ["Date&Time", 53, 60, 80, 90, 100, 110, 120, 140, 160, 180, 200]
list_columns = [list(Site_Daily_Wind_Speed.index), daily_mean_speed_dict['daily_mean_speed_53'], daily_mean_speed_dict['daily_mean_speed_60'], 
                daily_mean_speed_dict['daily_mean_speed_80'], daily_mean_speed_dict['daily_mean_speed_90'], 
                daily_mean_speed_dict['daily_mean_speed_100'], daily_mean_speed_dict['daily_mean_speed_110'], 
                daily_mean_speed_dict['daily_mean_speed_120'], daily_mean_speed_dict['daily_mean_speed_140'], 
                daily_mean_speed_dict['daily_mean_speed_160'], daily_mean_speed_dict['daily_mean_speed_180'], 
                daily_mean_speed_dict['daily_mean_speed_200']]
zipped_list = list(zip(list_labels, list_columns))
daily_wind_dict = dict(zipped_list)
Project_Site_Daily_Wind_Speed = pd.DataFrame(daily_wind_dict)
#declaring the index of the dataframe as date column
Project_Site_Daily_Wind_Speed = Project_Site_Daily_Wind_Speed.set_index("Date&Time")

#adding two dataframes together and sorting to have all daily wind speeds
All_Daily_Wind_Speeds = pd.concat([Predicted_Daily_Mean_Speed, Project_Site_Daily_Wind_Speed]) 
All_Daily_Wind_Speeds = All_Daily_Wind_Speeds.sort_index()

#reading the csv file that containts hourly wind speed data at project site
Site_Hourly_Wind_Speed = pd.read_csv("HourlyMeanSpeed.csv", index_col="Date&Time", parse_dates=True)

#creating dictionaries which stores days in months, and month order
day_dict = {'January':31, 'February':28, 'March':31, 'April':30, 'May':31, 'June':30, 'July':31, 'August':31, 'September':30, 'October':31, 'November':30, 'December':31}
month_dict = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}

#defining different turbine heights
turbine_height = [53, 60, 80, 90, 100, 110, 120, 140, 160, 180, 200]

years = ['2016','2017','2018'] 

for year in years:
    
#including December 2016 data
    if year == '2016': 
        months = ['December']
    else:
        months = ['January', 'February','March','April','May','June','July','August','September','October','November','December']
        
    for month in months:
        
        #creating a list for the number of days in that month
        day_numbers = list(range(1,int(day_dict[month]+1)))
        
        for height in turbine_height:
            
            #selecting the height column of hourly wind speed data
            Site_Hourly_Wind_Speed_h = Site_Hourly_Wind_Speed[str(height)]
                
            for day_no in day_numbers:
                
                #specifying consecutive days in this month
                specific_day = str(str(year)+'-'+str(month_dict[month])+'-'+str(day_no))
                #selecting the hourly mean data for that particular day
                specific_day_hourly_mean = Site_Hourly_Wind_Speed_h.loc[specific_day]
                #summing all hourly data in thet specific day
                Sum_Wind = specific_day_hourly_mean.sum()
                #transforming hourly data into a list
                Wind_List = list(specific_day_hourly_mean)
                #creating a new list that contains ratio of winds speeds to total wind speeds
                Ratio_List = [x/Sum_Wind for x in Wind_List]
                #adding ratio list to hourly profiles dictionary
                hourly_profiles_dict['hourly_profile_'+str(height)].append(Ratio_List)
                
#creating dictionaries which stores month order
month_dict = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}

#defining the years
years = [str(year_no) for year_no in range(1948,2017)]

for year in years:
    
    if int(year) % 4 == 0:
        day_dict= {'January':31, 'February':29, 'March':31, 'April':30, 'May':31, 'June':30, 'July':31, 'August':31, 'September':30, 'October':31, 'November':30, 'December':31}
    else:
        day_dict = {'January':31, 'February':28, 'March':31, 'April':30, 'May':31, 'June':30, 'July':31, 'August':31, 'September':30, 'October':31, 'November':30, 'December':31}
    if year == '2016': 
        months = ['January', 'February','March','April','May','June','July','August','September','October','November']
    else:
        months = ['January', 'February','March','April','May','June','July','August','September','October','November','December']

    for month in months:
        
        #finding the day numbers for every month
        day_numbers = list(range(1,int(day_dict[month]+1)))
        day_numbers = pd.Series(day_numbers)
        day_numbers = day_numbers.apply(lambda x:'{:0>2}'.format(x))
        day_numbers = list(day_numbers)
        
        for height in turbine_height:
            
            #selecting the height column of data
            Predicted_Daily_Mean_Speed_h = Predicted_Daily_Mean_Speed[height]
            Project_Site_Daily_Wind_Speed_h = Project_Site_Daily_Wind_Speed[height]
            
            for day_no in day_numbers:

                #specifying consecutive days in this month
                specific_day = str(str(year)+'-'+str(month_dict[month])+'-'+str(day_no))
                #selecting the daily mean data for that particular day
                specific_day_daily = Predicted_Daily_Mean_Speed_h.loc[specific_day]
                #turning selected data into a list
                Wind_List_Specific = list(Project_Site_Daily_Wind_Speed_h)
                #comparing selected daily wind speed with project site wind speeds
                Comparison_List = [abs(specific_day_daily - y) for y in Wind_List_Specific]
                #saving the index of the minimum difference in the comparison list
                Index_Min = Comparison_List.index(min(Comparison_List))
                #selecting hourly profile by using minimum difference index
                Selected_Profile = hourly_profiles_dict['hourly_profile_'+str(height)][Index_Min]
                #finding the specific days total wind speed by assuming wind speed were constant in that day
                specific_day_total = specific_day_daily * 24
                #generating hourly wind speeds by using selected profile
                Hourly_Generated_Speeds = [specific_day_total * z for z in Selected_Profile]
                #adding generated hourly data into dictionary
                hourly_generated_dict['predicted_hourly_final_'+str(height)].extend(Hourly_Generated_Speeds) 
                
#creating a temporary dataframe which includes all the hours in our data
data_time_range_hourly = list(pd.date_range('1948-01-01 00:00:00', '2016-11-30 23:00:00', freq='H'))
temporary_data_hourly=0   
temporary_dict_hourly = {"TempDate":data_time_range_hourly, "Data":temporary_data_hourly} 
temporary_dates_hourly = pd.DataFrame(temporary_dict_hourly)
temporary_dates_hourly = temporary_dates_hourly.set_index("TempDate")

#creating a dataframe for the generated hourly mean dataset
list_labels = ["Date&Time", 53, 60, 80, 90, 100, 110, 120, 140, 160, 180, 200]
list_columns = [list(temporary_dates_hourly.index), hourly_generated_dict['predicted_hourly_final_53'], hourly_generated_dict['predicted_hourly_final_60'], 
                hourly_generated_dict['predicted_hourly_final_80'], hourly_generated_dict['predicted_hourly_final_90'], 
                hourly_generated_dict['predicted_hourly_final_100'], hourly_generated_dict['predicted_hourly_final_110'], 
                hourly_generated_dict['predicted_hourly_final_120'], hourly_generated_dict['predicted_hourly_final_140'], 
                hourly_generated_dict['predicted_hourly_final_160'], hourly_generated_dict['predicted_hourly_final_180'], 
                hourly_generated_dict['predicted_hourly_final_200']]
zipped_list = list(zip(list_labels, list_columns))
hourly_wind_dict = dict(zipped_list)
Predicted_Hourly_Wind_Speed = pd.DataFrame(hourly_wind_dict)
#declaring the index of the dataframe as date column
Predicted_Hourly_Wind_Speed = Predicted_Hourly_Wind_Speed.set_index("Date&Time")  

for height in turbine_height:

    #selecting speed data for each hub height and saving them in a list
    Hub_Hourly_Mean_Speed = list(Site_Hourly_Wind_Speed[str(height)]) 
    #adding the data to the hub height specific lists in dictionaries
    hourly_site_dict['hourly_mean_speed_'+str(height)].extend(Hub_Hourly_Mean_Speed)
    
#creating a dataframe for the complete hourly site dataset
list_labels = ["Date&Time", 53, 60, 80, 90, 100, 110, 120, 140, 160, 180, 200]
list_columns = [list(Site_Hourly_Wind_Speed.index), hourly_site_dict['hourly_mean_speed_53'], hourly_site_dict['hourly_mean_speed_60'], 
                hourly_site_dict['hourly_mean_speed_80'], hourly_site_dict['hourly_mean_speed_90'], 
                hourly_site_dict['hourly_mean_speed_100'], hourly_site_dict['hourly_mean_speed_110'], 
                hourly_site_dict['hourly_mean_speed_120'], hourly_site_dict['hourly_mean_speed_140'], 
                hourly_site_dict['hourly_mean_speed_160'], hourly_site_dict['hourly_mean_speed_180'], 
                hourly_site_dict['hourly_mean_speed_200']]
zipped_list = list(zip(list_labels, list_columns))
hourly_wind_dict_site = dict(zipped_list)
Site_Hourly_Wind_Speed_new = pd.DataFrame(hourly_wind_dict_site)
#declaring the index of the dataframe as date column
Site_Hourly_Wind_Speed_new = Site_Hourly_Wind_Speed_new.set_index("Date&Time") 

#adding two dataframes together and sorting to have all hourly wind speeds
All_Hourly_Wind_Speeds = pd.concat([Predicted_Hourly_Wind_Speed, Site_Hourly_Wind_Speed_new]) 
All_Hourly_Wind_Speeds = All_Hourly_Wind_Speeds.sort_index()

#exporting data to a csv file
All_Daily_Wind_Speeds.to_excel("Historical_Daily_Wind_Speeds.xlsx")

#dropping all February 29ths
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2016-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2012-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2008-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2004-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('2000-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1996-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1992-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1988-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1984-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1980-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1976-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1972-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1968-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1964-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1960-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1956-02-29 23:00:00'), inplace=True)

All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 00:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 01:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 02:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 03:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 04:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 05:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 06:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 07:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 08:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 09:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 10:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 11:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 12:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 13:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 14:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 15:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 16:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 17:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 18:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 19:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 20:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 21:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 22:00:00'), inplace=True)
All_Hourly_Wind_Speeds.drop(pd.to_datetime('1952-02-29 23:00:00'), inplace=True)

#exporting data to a csv file
All_Hourly_Wind_Speeds.to_excel("Historical_Hourly_Wind_Speeds.xlsx")


