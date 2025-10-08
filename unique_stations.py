import pandas as pd
import os
import re
#import math
#import numpy as np

pd.options.mode.copy_on_write = True
pd.set_option("future.no_silent_downcasting", True)

#initialize year range and dataframes
csv_exclude = r'data.csv$'
year_start=1929
year_end=2025
year_list=list(map(str,range(year_start,year_end+1)))
year_set = set(year_list)
station_info=['STATION','NAME','LATITUDE','LONGITUDE']
unique_stations=pd.DataFrame(columns=station_info+year_list)

current_path = os.getcwd()
data_folder = 'weather_data'
data_path = os.path.join(current_path,data_folder)
year_list = [f.name for f in os.scandir(data_path) if f.is_dir() and f.name in year_set]

all_station_set = set()
for year in year_list:
    # print(f"\rIn: {year}                                 ", end = "", flush = True)
    # year="1948/"
    year_path = os.path.join(data_path,year)
    #create set of all csv files in each folder
    year_station_files = [f.name for f in os.scandir(year_path) if f.is_file() and not re.search(csv_exclude,f.name)]
    #print(csv_files)
    year_station_files_set = set(year_station_files)
    new_stations_set = year_station_files_set - all_station_set
    all_station_set = all_station_set | year_station_files_set
    new_stations = pd.DataFrame()
    for i, station in enumerate(new_stations_set):
        #print(weather_data_url+year+file)
        print(f"\rIn {year} Adding station: {station} Progress: {i+1}/{len(new_stations_set)}       ", end = "", flush = True)
        station_path = os.path.join(year_path,station)
        csv_df = pd.read_csv(station_path, dtype = {'STATION':'string'})
        csv_df.dropna(ignore_index=True,inplace=True)
        csv_df.drop_duplicates(subset=['STATION'],inplace=True)
        #print(csv_df.info())
        if new_stations.empty:
            new_stations = csv_df[station_info]
        else:
            new_stations=pd.concat([new_stations,csv_df[station_info]], ignore_index = True)
    #fix below to include previous stations, and not just unique stations in the current year
    # new_stations[f'{year}']=True

    if unique_stations.empty:
        unique_stations=new_stations
    #for all remaining loops, merge the year's unique stations with the unique stations master dataframe
    #all stations that previously existed have that year's column set to True, all new stations are added
    else:
        unique_stations=pd.merge(unique_stations,new_stations,how='outer',on=station_info)
    
    year_station_name_set = set([file.removesuffix('.csv') for file in year_station_files])
    # unique_stations['STATION']=unique_stations['STATION'].astype('string')
    unique_stations.loc[unique_stations['STATION'].isin(year_station_name_set) , f'{year}']=True
print('  Complete')
#clean up dataframe of unique stations, replace all 'NA' values with 'False'
unique_stations.reset_index(inplace=True,drop=True)
unique_stations.fillna(value=False,inplace=True)
#save dataframe
unique_stations.to_csv(f'All_Stations_{year_start}_{year_end}.csv',index=False)
print(f'All_Stations_{year_start}_{year_end}.csv save complete.')

