"""
Data Ingestion Methods

Contains functions to ingest data from a file and format it
"""

__date__ = "2023-11-10"
__authors__ = "NedeeshaWeerasuriya"
__version__ = "0.1"

# Import required libraries
import numpy as np
import pandas as pd
import requests
from pyowm import OWM
from pyproj import Proj, Transformer

# Import helper functions
from src.helpers.time_tracker import track_time
from src.helpers.utils import is_number


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
def call_api(url: str, headers: dict = None, params: dict = None) -> dict:
    """
    Call an API and return the response as JSON
    """
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        return response.json()  # Return the response data as JSON
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None


@track_time
def convert_easting_northing_to_long_lat(easting: int, northing: int) -> tuple:
    """
    Convert easting and northing coordinates to longitude and latitude
    """
    inProj = Proj("epsg:27700")
    outProj = Proj("epsg:4326")
    latitude, longitude = Transformer.from_proj(inProj, outProj).transform(
        easting, northing
    )
    return latitude, longitude


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
