# Project Name: Finding Mjolnir
See Mjolnir Group Presentation.pptx for images and more in-depth discussion
## Project Overview
Project Prompt: Mjolnir (Thor’s Hammer) fell on earth and was covered up as a normal meteorite landing. Since Thor is the god of thunder, his hammer’s arrival is assumed to be accompanied by thunderstorms.  
Goal: Find weather stations in range (10 miles) of meteorite landings and determine if there were more thunderstorms than normal around the time when the meteorite landed.  
Selection Criteria 1: The number of local thunderstorms in the year the meteorite landed is 10 or more above a 10 year average  
Selection Criteria 2: The number of local thunderstorms in the year the meteorite landed is over 50% more than a 10 year average  
The following two datasets were used:  
National Centers for Environmental Information Global Surface Summary of Day Data (GSOD)  
NASA comprehensive data set of Meteorite Landings from The Meteorological Society  


## Technologies Used
- Python
- pandas
- numpy
- BeautifulSoup
- folium (interactive map)
- matplotlib

## Project Objectives
- Demonstrate automated web scraping using requests and BeautifulSoup
- Demonstrate data analysis using pandas
- Demonstrate data presentation through folium and matplotlib

## Features
- Automatically scrapes GSOD data from www.ncei.noaa.gov  
- Calculates thunderstorm occurances and averages in all weather stations
- Finds active weather stations in range of meteorite landings
- Finds abnormal levels of thunderstorms in year of meteorite landing to identify potential Mjolnir candidates
- Creates interactive map of Mjolnir Candidates and relevant plots

## Prerequisites
- Python 3.x
- Virtual Environment
- Required dependencies (list in requirements.txt)

## Installation

### Clone the Repository
git clone https://github.com/Jollyfalcon/Mjolnir  
cd project-directory

### Set Up Virtual Environment
python -m venv venv  
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

### Install Dependencies
pip install -r requirements.txt

### Running the Application
 - TBD

### Running Tests
 - TBD

### Project Structure
project-directory/  
│  
├── Weather_Data/  
│ ├── Weather_Data.ipynb  
│ └── Total_Weather_Files.ipynb  
├── Mjolnir.ipynb  
├── Meteorite_Plots.ipynb  
├── Mjolnir_Candidates.ipynb  
├── Candidate Meteorite Details.xlsx  
├── Product Backlog and Sprints.xlsx  
├── Mjolnir Group Presentation.pptx  
├── Meteorite_Landings.csv  
├── requirements.txt  
└── README.md

## Learning Outcomes
Advanced Python programming  
Webscraping, HTML syntax, data collection automation  
Data cleaning, manipulation, merging, and analysis  
Data presentation  

## License
MIT License

## Contact
Joshua Stuckey  
email: stuckeyjp1@gmail.com  
LinkedIn: https://www.linkedin.com/in/joshua-stuckey/
