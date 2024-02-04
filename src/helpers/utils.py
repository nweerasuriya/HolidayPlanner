"""
Utilities for the project
"""

__date__ = "2023-11-10"
__author__ = "NedeeshaWeerasuriya"

import os

import geopy.distance
import numpy as np
from pyproj import Proj, Transformer


def create_folder(directory: str) -> str:
    """
    Create a given folder if fit does not exit
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)
    return directory


def is_number(s) -> bool:
    """
    Checks if a variable is float or complex
    """
    try:
        float(s)  # for int, long and float
    except ValueError:
        try:
            complex(s)  # for complex
        except ValueError:
            return False

    return True


def check_substr_in_dict(x: dict, substr: str) -> str:
    """
    Check if the substring exists in the dictionary keys
    """
    for key in x.keys():
        if substr in key:
            return x[key]
    return np.nan


def relative_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the relative distance between two points on the Earth's surface using geopy.
    Uses the Vincenty distance which has more accurate ellipsoidal models, such as WGS-84.
    """
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geopy.distance.distance(coords_1, coords_2).km


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
