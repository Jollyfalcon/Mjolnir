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
    station_data_df = pd.read_csv(station_data_path)
    thunder_counts_df = {}
    year_list = list(map(str,range(G_START_DATE,G_END_DATE)))
    year_set = set(year_list)
    year_list_found = [f.name for f in os.scandir(G_DATA_PATH) if f.is_dir() and f.name in year_set]
    for year in year_list_found:
        year_path = os.path.join(G_DATA_PATH,str(year))
        thunder_counts_df[year]=pd.read_csv(year_path)
    
    #begin average analysis
    for year in year_list_found:
        print(f"\rProcessing Thunder averages in {year}: ", end = "", flush = True)
        year_path = os.path.join(G_DATA_PATH,str(year))
        file_name = f'{year}_thunder_averages.csv'
        file_path = os.path.join(year_path,file_name)
        if os.path.isfile(file_path): continue
        thunder_counts_df[year]['Thunder Average'] = thunder_counts_df.apply(
            lambda x: calc_thunder_avg(x['STATION'],
                                       year,
                                       thunder_counts_df[year],
                                       station_data_df
                                       ),
                                       axis=1,result_type='expand')
        thunder_counts_df[year].to_csv(file_path,index = False)
        print('Complete')

def calc_thunder_avg(station,date,thunder_counts,station_data_df) -> float:
    #creating a list of years with sufficient data for a moving 10 year average
    year_list = []
    initial_start = date - 5
    initial_end = date + 5
    #edge cases of bookend years
    if initial_start < G_MIN_DATE:
        initial_start = G_MIN_DATE
        initial_end = initial_start + 11
    elif initial_end > G_MAX_DATE:
        initial_end = G_MAX_DATE
        initial_start = initial_end - 11
    #finding all years with minimum amount of data points
    for year in range(initial_start,initial_end):
        if year==date: continue
        if station_data_df[station_data_df['STATION'==station]][year]>=G_MIN_DATA_POINTS:
            year_list.add(date)
    #if 5 preceeding and 5 following years do not have sufficient data, check the next
    #furthest out years until 10 years with sufficient data points are found
    extend_start = initial_start-1
    extend_end = initial_end+1
    while len(year_list)<10:
        if extend_start >= G_MIN_DATE:
            if station_data_df[station_data_df['STATION'==station]][extend_start]>=G_MIN_DATA_POINTS:
                year_list.add(extend_start)
                extend_start -= 1
        if len(year_list)==10: break
        if extend_end <= G_MAX_DATE:
            if station_data_df[station_data_df['STATION'==station]][extend_end]>=G_MIN_DATA_POINTS:
                year_list.add(extend_end)
                extend_end += 1
        #if search extends too far in either direction, end the search
        if extend_start <= initial_start - G_MAX_SEARCH or extend_end >= initial_end + G_MAX_SEARCH: break
    
    weighted_counts = []
    for year in year_list:
        station_thunder = thunder_counts[thunder_counts['STATION'==station]]['THUNDER INSTANCES']
        station_data_points = thunder_counts[thunder_counts['STATION'==station]]['DATA POINTS']
        weighted_counts.append(station_thunder*station_data_points)
        #confused on the best approach to this calculation - how to address leap years?
        #should I calculate a weighted daily average? [thunder_counts]/[data_points]
        #if I try to calculate a weighted yearly average, [thunder_counts]/[data_points]*[365 OR 366]
        #then leap years will be slightly over representative in the 10 year running average
        #do I want each year to be equal, or to give the leap years a bit more weight?
    
if __name__ == "__main__":
    main()
