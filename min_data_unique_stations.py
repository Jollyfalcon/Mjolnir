import pandas as pd
import os
#import math
#import numpy as np

pd.options.mode.copy_on_write = True
pd.set_option("future.no_silent_downcasting", True)

#initialize year range and dataframes
min_data_points = 190
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
    year_station_files = [f.name for f in os.scandir(year_path) if f.is_file()]
    year_station_info = station_info + [f'{year}']
    #print(csv_files)
    year_station_data_set = set()
    stations_with_data = pd.DataFrame(columns=station_info)
    for i, station in enumerate(year_station_files):
        #print(weather_data_url+year+file)
        print(f"\rIn {year} adding station: {station} Progress: {i+1}/{len(year_station_files)}       ", end = "", flush = True)
        station_path = os.path.join(year_path,station)
        csv_df = pd.read_csv(station_path, dtype = {'STATION':'string'})
        csv_df.dropna(ignore_index=True,inplace=True)
        station_data_points = len(csv_df)
        csv_df.drop_duplicates(subset=['STATION'],inplace=True)
        csv_df[f'{year}'] = station_data_points
        #print(csv_df.info())
        if station_data_points>min_data_points:
            year_station_data_set.add(station.removesuffix('.csv'))
        if stations_with_data.empty:
            stations_with_data = csv_df[year_station_info]
        else:
            stations_with_data=pd.concat([stations_with_data,csv_df[year_station_info]], ignore_index = True)
    #fix below to include previous stations, and not just unique stations in the current year
    # new_stations[f'{year}']=True

    if unique_stations.empty:
        unique_stations=stations_with_data
    #for all remaining loops, merge the year's unique stations with the unique stations master dataframe
    #all stations that previously existed have that year's column set to True, all new stations are added
    else:
        unique_stations=pd.merge(unique_stations,stations_with_data,how='outer',on=station_info)
    
    # unique_stations['STATION']=unique_stations['STATION'].astype('string')
    # if not unique_stations.empty:
    #     unique_stations.loc[unique_stations['STATION'].isin(year_station_data_set) , f'{year}']=True
print('  Complete')
#clean up dataframe of unique stations, replace all 'NA' values with 'False'
unique_stations.reset_index(inplace=True,drop=True)
unique_stations.fillna(value=0,inplace=True)
#save dataframe
unique_stations.to_csv(f'YearlyStationDataPoints_{year_start}_{year_end}.csv',index=False)
print(f'YearlyStationDataPoints_{year_start}_{year_end}.csv save complete.')

