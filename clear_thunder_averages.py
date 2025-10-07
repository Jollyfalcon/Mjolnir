#clears weather_data folder of all [year]_thunder_avg_data.csv files

#includes
import os

#constants
G_START_DATE = 1929
G_END_DATE = 2025

#path
G_CURR_PATH = os.getcwd()
G_DATA_PATH = os.path.join(G_CURR_PATH,'weather_data')

def main():
    year_list = range(G_START_DATE,G_END_DATE+1)
    year_list_str = list(map(str,year_list))
    year_set = set(year_list_str)
    year_list_found = [f.name for f in os.scandir(G_DATA_PATH) if f.is_dir() and f.name in year_set]
    
    #begin average analysis
    for year in year_list_found:
        year_path = os.path.join(G_DATA_PATH,str(year))
        file_name = f'{year}_thunder_avg_data.csv'
        file_path = os.path.join(year_path,file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f'Removed {year}\{file_name}')

if __name__ == '__main__':
    main()