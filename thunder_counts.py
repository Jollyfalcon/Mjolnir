import pandas as pd
import os
import re

pd.options.mode.copy_on_write = True
pd.set_option("future.no_silent_downcasting", True)

#initialize year range and dataframes
csv_exclude = r'data.csv$'
year_start=1929
year_end=2025
year_list=list(map(str,range(year_start,year_end+1)))
year_set = set(year_list)
station_info=['STATION','NAME','LATITUDE','LONGITUDE','THUNDER INSTANCES','DATA POINTS']

current_path = os.getcwd()
data_folder = 'weather_data'
data_path = os.path.join(current_path,data_folder)
year_list = [f.name for f in os.scandir(data_path) if f.is_dir() and f.name in year_set]

for year in year_list:
    # print(f"\rIn: {year}                                 ", end = "", flush = True)
    # year="1948/"
    thunder_data=pd.DataFrame(columns=station_info)
    year_path = os.path.join(data_path,year)
    file_name = f'{year}_thunder_data.csv'
    file_path = os.path.join(year_path,file_name)
    if os.path.isfile(file_path):
        continue
    #create set of all csv files in each folder
    year_station_files = [f.name for f in os.scandir(year_path) if f.is_file() and not re.search(csv_exclude,f.name)]
    
    i=0
    for station in year_station_files:
        #print(weather_data_url+year+file)
        i+=1
        print(f"\rThunder counts for {station} in {year}. Progress: {i}/{len(year_station_files)}             ", end = "", flush = True)
        station_path = os.path.join(year_path,station)
        csv_df = pd.read_csv(station_path, dtype = {'STATION':'string'})
        csv_df.dropna(ignore_index=True,inplace=True)
        thunder_instances = len(csv_df[(csv_df['FRSHTT']//10)%2==1])
        data_points = len(csv_df)
        csv_df.drop_duplicates(subset=['STATION'],inplace=True)
        csv_df['THUNDER INSTANCES'] = thunder_instances
        csv_df['DATA POINTS'] = data_points
        if thunder_data.empty:
            thunder_data = csv_df[station_info]
        else:
            thunder_data = pd.concat([thunder_data,csv_df[station_info]], ignore_index = True)
    #save dataframe
    thunder_data.to_csv(file_path,index=False)
    print(f'\n{file_name} in /{year}/ folder save complete.')
print('Complete')
