#%%------
import datetime as dt
import sys

# change working directory to the root of the project

sys.path.append('../')
from src.methods.data_ingestion import call_api

# longitude = input("Please provide a longitute: ")
# latitude = input("Please provide a latitutde: ")
# date_and_time_string = input('Enter Date and time in following format YYYY-MM-DD HH:MM')

#%%--------
""" Longitude North / South 
    Latitude West / East
    
    
    
Key components we care about: 
- 2 OPTIONS : EITHER A DAY COMPONENT OR HOURLY COMPONENT
* Chance of rain
* Sunny/Cloud level -> Image 
* Wind ( if wind is more than 25 km than needs to be flat)
* Temperature (if Day than MAX POINT)

FLAGS for No to outdoor activity : 
* Rain chance > 50% 
* Wind > 25kmph / 18mph
* Temperature outside of [10-27 degrees] maybe some activities can be omitted"""

from datetime import datetime

#Location for SE10 London (Greenwich)
longitude = '51.4808'
latitude = '0.0029'





def open_meteo_api(lon,lat):
    params = {
        "latitude": lat,
	    "longitude": lon,
        "current": ["temperature_2m", "precipitation", "weather_code", "wind_speed_10m"],
	    "hourly": ["temperature_2m", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "wind_speed_10m", "wind_direction_10m"]

	    #temperature_2m - stands for air temperature at 2 meters above ground
        #precipitation - total precipitation in mm in the preceeding hour
        #weather code
        #wind_speed_10m - windspeed at 10 meters above ground
        #rain - measured in sum of mm in the preceding hours
    }
    
    response = call_api('https://api.open-meteo.com/v1/forecast',params=params)
    return response

response = open_meteo_api(longitude,latitude)
print(f"Coordinates {response['latitude']}°E {response['longitude']}°N")
print(f"Elevation {response['elevation']} m asl")
print(f"Timezone {response['timezone']} {response['timezone_abbreviation']}")
print(f"Timezone difference to GMT+0 {response['utc_offset_seconds']} s")


# Current values. The order of variables needs to be the same as requested.
current = response['current']
current_temperature_2m = response['current']['temperature_2m']
current_precipitation = response['current']['precipitation']
current_weather_code = response['current']['weather_code']
current_wind_speed_10m = response['current']['wind_speed_10m']

"""Weather code follows: WMO 
https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM

provides a code for every sitauation
"""

print(f"Current time {current['time']}")
print(f"Current temperature_2m {current_temperature_2m}")
print(f"Current precipitation {current_precipitation}")
print(f"Current weather_code {current_weather_code}")
print(f"Current wind_speed_10m {current_wind_speed_10m}")


# %%
