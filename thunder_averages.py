#create a dictionary that contains all [year]_thunder_data.csv as dataframes
#should fit in memory just fine
#can loop through and perform calculations without opening new files
#make the lambda function as simple as possible
#consider the effect of sample size on using data with low amounts of data points

#includes
import os
import pandas as pd

#constants
G_MIN_DATA_POINTS = 190
G_MIN_DATA_YEARS = 6
G_MIN_DATE = 1929
G_MAX_DATE = 2025
G_MAX_SEARCH = 10

G_START_DATE = 1929
G_END_DATE = 2025

#path
G_CURR_PATH = os.getcwd()
G_DATA_PATH = os.path.join(G_CURR_PATH,'weather_data')

def main():
    #load all relevant data
    station_data_name = 'YearlyStationDataPoints_1929_2025.csv'
    station_data_path = os.path.join(G_CURR_PATH,station_data_name)
    station_data_df = pd.read_csv(station_data_path, dtype = {'STATION':'string'})
    thunder_counts_df = {}
    all_years_list = range(G_MIN_DATE,G_MAX_DATE+1)
    all_years_list_str = list(map(str,all_years_list))
    all_years_set = set(all_years_list_str)
    all_years_list_found = [f.name for f in os.scandir(G_DATA_PATH) if f.is_dir() and f.name in all_years_set]
    for year in all_years_list_found:
        year_path = os.path.join(G_DATA_PATH,str(year))
        thunder_counts_path = os.path.join(year_path,f'{year}_thunder_data.csv')
        thunder_counts_df[year]=pd.read_csv(thunder_counts_path, dtype = {'STATION':'string'})
    
    year_list = range(G_START_DATE,G_END_DATE+1)
    year_list_str = list(map(str,year_list))
    year_set = set(year_list_str)
    year_list_found = [f.name for f in os.scandir(G_DATA_PATH) if f.is_dir() and f.name in year_set]
    
    #begin average analysis
    for year in year_list_found:
        year_path = os.path.join(G_DATA_PATH,str(year))
        file_name = f'{year}_thunder_avg_data.csv'
        file_path = os.path.join(year_path,file_name)
        if os.path.isfile(file_path): continue
        thunder_counts_df[year]['Thunder Average'] = thunder_counts_df[year].apply(
            lambda x: calc_thunder_avg(x.name,
                                       x['STATION'],
                                       year,
                                       thunder_counts_df,
                                       station_data_df
                                       ),
                                       axis=1,result_type='expand')
        thunder_counts_df[year].to_csv(file_path,index = False)
        print('Complete')

def calc_thunder_avg(station_index,
                     station,date,
                     thunder_counts,
                     station_data_df
                     ) -> float:
    
    station_total = len(thunder_counts[date])
    print(f"\rProcessing Thunder averages in {date}: {station_index+1}/{station_total} ", end = "", flush = True)

    #creating a list of years with sufficient data for a moving 10 year average
    year_list = []
    date_int = int(date)
    initial_start = date_int - 5
    initial_end = date_int + 5
    #edge cases of bookend years
    if initial_start < G_MIN_DATE:
        initial_start = G_MIN_DATE
        initial_end = initial_start + 11
    elif initial_end > G_MAX_DATE:
        initial_end = G_MAX_DATE
        initial_start = initial_end - 11
    #finding all years with minimum amount of data points
    for year in range(initial_start,initial_end+1):
        year_data_points = station_data_df.loc[station_data_df['STATION']==station,[str(year)]].values[0]
        # print(year_data_points)
        if year==date_int: continue
        if year_data_points>=G_MIN_DATA_POINTS:
            year_list.append(year)
    #if 5 preceeding and 5 following years do not have sufficient data, check the next
    #furthest out years until 10 years with sufficient data points are found
    # print(year_list)
    extend_start = initial_start-1
    extend_end = initial_end+1
    while len(year_list)<10:
        if extend_start >= G_MIN_DATE:
            station_extension_start = station_data_df.loc[station_data_df['STATION']==station,[str(extend_start)]].values[0]
            if station_extension_start >= G_MIN_DATA_POINTS:
                year_list.append(extend_start)
        extend_start -= 1
        if len(year_list)==10: break
        if extend_end <= G_MAX_DATE:
            station_extension_end = station_data_df.loc[station_data_df['STATION']==station, [str(extend_end)]].values[0]
            if station_extension_end >= G_MIN_DATA_POINTS:
                year_list.append(extend_end)
        extend_end += 1
        #if search extends too far in either direction, end the search
        if extend_start <= initial_start - G_MAX_SEARCH or extend_end >= initial_end + G_MAX_SEARCH: break
    
    weighted_counts = []
    # print(station)
    # print(year_list)
    for year in year_list:
        station_thunder = thunder_counts[str(year)].loc[thunder_counts[str(year)]['STATION']==station,['THUNDER INSTANCES']].values[0]
        station_data_points = thunder_counts[str(year)].loc[thunder_counts[str(year)]['STATION']==station,['DATA POINTS']].values[0]
        weighted_counts.append(station_thunder/station_data_points*365)
        #confused on the best approach to this calculation - how to address leap years?
        #should I calculate a weighted daily average? [thunder_counts]/[data_points]
        #if I try to calculate a weighted yearly average, [thunder_counts]/[data_points]*[365 OR 366]
        #then leap years will be slightly over representative in the 10 year running average
        #do I want each year to be equal, or to give the leap years a bit more weight?
    if len(weighted_counts)>=G_MIN_DATA_YEARS:
        thunder_average = sum(weighted_counts)/len(weighted_counts)
    else:
        thunder_average = None
    return thunder_average
    
if __name__ == "__main__":
    main()
