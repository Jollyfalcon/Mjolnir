import os
import re

#initialize year range and dataframes
csv_exclude = r'data.csv$'
year_start=1929
year_end=2025
year_list=list(map(str,range(year_start,year_end+1)))
year_set = set(year_list)

current_path = os.getcwd()
data_folder = 'weather_data'
data_path = os.path.join(current_path,data_folder)
year_list = [f.name for f in os.scandir(data_path) if f.is_dir() and f.name in year_set]

num_files=0
for year in year_list:
    # print(f"\rIn: {year}                                 ", end = "", flush = True)
    # year="1948/"
    year_path = os.path.join(data_path,year)
    #create set of all csv files in each folder
    year_station_files = [f.name for f in os.scandir(year_path) if f.is_file() and not re.search(csv_exclude,f.name)]
    total_files = len(year_station_files)
    print(f"\rAdding {total_files} from year {year} to {num_files}         ", end = "", flush = True)
    num_files=num_files+total_files

print('Complete')
print(f'Total number of csv files is {num_files}')

