import datetime 
import sys


# change working directory to the root of the project
sys.path.append('../')
from src.methods.data_ingestion import call_api

longitude = input("Please provide a longituted")
latitude = input("Please provide a latitutde")
date_and_time_string = input('Enter Date and time in following format YYYY-MM-DD HH:MM')

def i_want_to_know_the_weather(lat,lon,date_and_time:str):
    date_and_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    params = {
        "latitude": lat,
	    "longitude": lon,
	    "hourly":  ["temperature_2m",           #temperature_2m - stands for air temperature at 2 meters above ground
                    "precipitation",			#precipitation - total precipitation in mm in the preceeding hour
                    "rain"]} 					#rain - measured in sum of mm in the preceding hours
    
    response = call_api('https://api.open-meteo.com/v1/forecast')

    index_= response['hourly'].index(date_and_time)

    print(f'''At your destination there is an estimated:
          - {response['hourly']['temperature_2m'][index_]}' degrees 
          - {response['hourly']['rain'][index_]},'mm of rain? 
          - {response['hourly']['precipitation'][index_]},'expected precipitation''')
    
    i_want_to_know_the_weather(latitude,longitude,date_and_time_string)

"""Quetions to ask: (by Kenny)
- do we want to retrieve and store all the data Y/N
- How will the API interract with the other API ? 
- What details/parameters shall I focus on and aim to retrieve?  """
