import os
import tarfile

curr_path = os.getcwd()
data_dir = 'weather_data'
data_path = os.path.join(curr_path,data_dir)
archive_dir = 'zipped_data'
archive_path = os.path.join(curr_path,data_dir,archive_dir)
print(archive_path)
os.makedirs(archive_path,exist_ok = True)

zip_files = [f.name for f in os.scandir(archive_path) if f.is_file()]
iterator=0
for file_name in zip_files:
    iterator+=1
    print(f"\rUnzipping: {file_name} Progress: {iterator}/{len(zip_files)}          ", end = "", flush = True)
    file_path = os.path.join(archive_path,file_name)
    year_name = file_name.removesuffix(".tar.gz")
    year_path = os.path.join(data_path,year_name)
    file = tarfile.open(file_path)
    os.makedirs(year_path, exist_ok = True)
    file.extractall(year_path,filter='data')
    file.close
print('Complete')