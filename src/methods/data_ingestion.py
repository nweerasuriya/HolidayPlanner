"""
Data Ingestion Methods

Contains functions to ingest data from a file and format it
"""

__date__ = "2023-11-10"
__authors__ = "NedeeshaWeerasuriya, Sang Nguyen"
__version__ = "0.1"

<<<<<<< HEAD
"""
Import Modules
"""
=======
# Import required libraries
>>>>>>> b1efb45c14fb64277eda07bd70ff62a0ad0a775b
import numpy as np
import pandas as pd
import requests
from pyowm import OWM

<<<<<<< HEAD
from enum import Enum
=======
# Import helper functions
>>>>>>> b1efb45c14fb64277eda07bd70ff62a0ad0a775b
from src.helpers.time_tracker import track_time
from src.helpers.utils import is_number

"""
Enums
"""
Request = Enum('Request', ['GET','POST'])

@track_time
def format_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Checks and formats the time and value columns
    """
    filter_num = df["value"].apply(lambda x: is_number(x))
    df.loc[~filter_num] = np.nan

    df[["value"]] = df[["value"]].apply(pd.to_numeric)
    df["time"] = pd.to_datetime(
        df["time"], format="%Y-%m-%d %H:%M:%S.%f"
    )  # , errors='coerce')
    df = df.sort_values(by="time", ascending=True)
    df.set_index(["time"], inplace=True)

    # final checks for duplicates and NaNs
    df = df.loc[~df.index.duplicated()]
    df.dropna(inplace=True)

    return df


@track_time
def filter_data_ranges(data: pd.DataFrame, data_range: tuple) -> pd.DataFrame:
    """
    Filter data based on specified ranges
    """
    # Filter lower values
    data = data.loc[data.values >= data_range[0]]
    # Filter upper values
    data = data.loc[data.values <= data_range[1]]
    return data


@track_time
<<<<<<< HEAD
def call_api(url: str, headers: dict = None, params: dict = None, request: Request = Request.GET):
    """
    Performs a REST API call and returns the response

    Params
    ------
    url: str
        The request url
    headers: dict
        A dictionary of request headers
    params: dict
        A dictionary of parameters in the request body
    request: Request
        The REST method used in the API call, must be a valid item in the Request Enum
=======
def call_api(url: str, headers: dict = None, params: dict = None) -> dict:
    """
    Call an API and return the response as JSON
>>>>>>> b1efb45c14fb64277eda07bd70ff62a0ad0a775b
    """
    try:
        if request == Request.GET:
            response = requests.get(url, headers=headers, params=params)
        elif request == Request.POST:
            response = requests.post(url, headers=headers, data=params)
        else:
            raise requests.exceptions.RequestException("Invalid request method")

        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        return response.json()  # Return the response data as JSON
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
<<<<<<< HEAD
        return 
=======
        return None


@track_time
def get_openweather(lat: float, lon: float, api_key="3201bd50938164da1d0f66147bde4f78"):
    """
    Get current weather and forecast for a location using OpenWeatherMap API
    """
    owm = OWM(api_key)
    mgr = owm.weather_manager()
    # Get current weather
    observation = mgr.weather_at_coords(lat=lat, lon=lon)
    # Get forecast
    forecast = mgr.forecast_at_coords(lat=lat, lon=lon, interval="3h")
    return observation, forecast


@track_time
def format_forecast_openweather(forecast: dict) -> pd.DataFrame:
    """
    Format the forecast data from OpenWeatherMap API and return a DataFrame with the relevant information
    """
    weather_list = forecast["weathers"]
    output_dict = {}
    for weather_dict in weather_list:
        # convert reference time to datetime
        weather_dict["reference_time"] = pd.to_datetime(
            weather_dict["reference_time"], unit="s"
        )
        # convert kelvin to celsius
        temp = int(weather_dict["temperature"]["temp"] - 273.15)
        output_dict[weather_dict["reference_time"]] = {
            "temperature (C)": temp,
            "detailed_status": weather_dict["detailed_status"],
            "wind (mph)": weather_dict["wind"]["gust"],
        }
    # remove timestamps keys before 7am and after 10pm
    forecast_dict = {
        k: v for k, v in output_dict.items() if k.hour >= 7 and k.hour <= 22
    }

    weather_df = pd.DataFrame(forecast_dict).T
    # Get day of the week as column
    weather_df["day_of_week"] = weather_df.index.day_name()
    # Creat grouping in weather dataframe for Morning (9am-12pm), Noon (12pm-3pm), Afternoon (3pm-6pm), Evening (6pm-9pm)
    weather_df["time_of_day"] = pd.cut(
        weather_df.index.hour,
        bins=[6, 9, 12, 15, 18, 21],
        labels=["Morning", "Noon", "Afternoon", "Evening", "Night"],
    )
    return weather_df
>>>>>>> b1efb45c14fb64277eda07bd70ff62a0ad0a775b
