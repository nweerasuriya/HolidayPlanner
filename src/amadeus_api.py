"""
Data Ingestion Script for Amadeus API

"""

__date__ = "2023-12-03"
__author__ = "Sang Nguyen"
__version__ = "0.1"


# %% --------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
import sys
from pathlib import Path

sys.path.append("../")

import json
import pandas as pd
from src.methods.data_ingestion import call_api, Request
from src.helpers.utils import relative_distance


# %% --------------------------------------------------------------------------
# Main Script
# -----------------------------------------------------------------------------
def default_params() -> dict:
    """
    Default parameters for the Amadeus API
    """
    request_params = {
        "latitude": "51.484703",
        "longitude": "-0.061048",
        "radius": "5",
        "categories": "SIGHTS",
    }

    return request_params


def get_auth_token(auth_url: str, client_id: str, client_secret: str) -> str:
    """
    Retrieves an authentication token from the Amadeus API

    Params
    ------
    auth_url: str
        The url used in the api call for authentication
    client_id: str
        The Client ID of the Amadeus API App
    client_secret: str
        The Client Secret of the Amadeus API App
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    request_params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    res = call_api(
        url=auth_url, headers=headers, params=request_params, request=Request.POST
    )

    return res["access_token"]


def format_amadeus_data(
    res_api: dict, param_lat: float, param_long: float
) -> pd.DataFrame:
    """
    Retrieves an authentication token from the Amadeus API

    Params
    ------
    res_api: dict
        The resulting dictionary from the api call
    param_lat: float
        The latitude parameter supplied to the api call
    param_long: float
        The longitude parameter supplied to the api call
    """
    df = pd.DataFrame(
        res_api["data"], columns=["name", "category", "geoCode", "rank", "tags"]
    )
    df = pd.concat(
        [df.drop(["geoCode"], axis=1), df["geoCode"].apply(pd.Series)], axis=1
    )

    df["distance"] = df.apply(
        lambda x: relative_distance(
            lat1=param_lat, lon1=param_long, lat2=x.latitude, lon2=x.longitude
        ),
        axis=1,
    )

    df = df[["name", "category", "latitude", "longitude", "distance", "rank", "tags"]]
    df = df.set_index("name")

    return df


def amadeus_pipeline(request_params: dict = default_params(), isProd: bool = False):
    """
    Pipeline for the Amadeus API - Points of Interest

    Params
    ------
    request_params: str
        The parameters to be supplied to the api request
    isProd: bool
        A boolean defining if the api call should be to the prod environment
    """
    env_str = "prod" if isProd else "dev"

    config_path = f"{Path(__file__).resolve().parent}/config.json"

    with open(config_path, "r") as config_file:
        config = json.load(config_file)["amadeus_api"][env_str]

    auth_token = get_auth_token(
        config["auth_url"], config["client_id"], config["client_secret"]
    )

    url = config["poi_url"]

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    res = call_api(url=url, headers=headers, params=request_params, request=Request.GET)

    activities_df = format_amadeus_data(
        res_api=res,
        param_lat=request_params["latitude"],
        param_long=request_params["longitude"],
    )

    return activities_df
