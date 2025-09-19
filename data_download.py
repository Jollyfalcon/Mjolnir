# import libraries to request data from URLs and read them
import requests
from bs4 import BeautifulSoup
import os

year_start = 1929
year_end = 2025
year_range = range(year_start,year_end+1)
file_set = set([str(year)+'.tar.gz' for year in year_range])

#directory management
current_path = os.getcwd()
data_folder = 'weather_data'
archive_folder = 'zipped_data'
archive_path = os.path.join(current_path,data_folder,archive_folder)
os.makedirs(archive_path, exist_ok=True)

#URL of directory of weather data
weather_data_url = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/"
#get HTML text from ULR
url_text = requests.get(weather_data_url)
#use Beautiful Soup to parse data in HTML text
weather_soup = BeautifulSoup(url_text.text,'html.parser')

#create list of all year folders containing .csv files 
href_values = [a['href'] for a in weather_soup.find_all('a', href=True)]
# print(href_values)
all_files = [href for href in href_values if href in file_set]
# print(year_folders)

for i, file in enumerate(all_files):
    print(f"\rDownloading: {file} Progress: {i+1}/{len(all_files)}             ", end = "", flush = True)

    url = weather_data_url + file
    file_path = os.path.join(archive_path,file)
    if os.path.isfile(file_path):
        continue
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=4*1024*1024): # 4 MB chunks
                if chunk: # Filter out keep-alive chunks
                    file.write(chunk)

print('Complete')