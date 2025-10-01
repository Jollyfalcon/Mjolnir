#create a dictionary that contains all [year]_thunder_data.csv as dataframes
#should fit in memory just fine
#can loop through and perform calculations without opening new files
#make the lambda function as simple as possible
#consider the effect of sample size on using data with low amounts of data points

#constants
G_MIN_DATA_POINTS = 190
G_MIN_DATE = 1929
G_MAX_DATE = 2025

def calc_thunder_average(station,date) -> float:
    global thunder_counts
    global station_data_points

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
        if station_data_points[station_data_points['STATION'==station]][year]>=G_MIN_DATA_POINTS:
            year_list.add(date)
    #if 5 preceeding and 5 following years do not have sufficient data, check the next
    #furthest out years until 10 years with sufficient data points are found
    extend_start = initial_start-1
    extend_end = initial_end+1
    while len(year_list)<10:
        if extend_start >= G_MIN_DATE:
            if station_data_points[station_data_points['STATION'==station]][extend_start]>=G_MIN_DATA_POINTS:
                year_list.add(extend_start)
                extend_start -= 1
        if len(year_list)==10: break
        if extend_end <= G_MAX_DATE:
            if station_data_points[station_data_points['STATION'==station]][extend_end]>=G_MIN_DATA_POINTS:
                year_list.add(extend_end)
                extend_end += 1
        #if not enough years with data points are found, end the search
        if extend_start <= G_MIN_DATE and extend_end >= G_MAX_DATE: break

    

