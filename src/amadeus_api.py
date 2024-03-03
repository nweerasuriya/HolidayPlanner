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
sys.path.append('../')

import json
import pandas as pd
from src.methods.data_ingestion import call_api, Request
from src.helpers.utils import relative_distance


# %% --------------------------------------------------------------------------
# Main Script
# -----------------------------------------------------------------------------
def default_parameters() -> dict:
    request_params = {
        "latitude": "51.484703",
        "longitude": "-0.061048",
        "radius": "5",
        "categories": "SIGHTS"
    }

    return request_params

def get_auth_token(config: dict) -> str:
    url = config['auth_url']

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request_params = {
        "grant_type": "client_credentials",
        "client_id": config['client_id'],
        "client_secret": config['client_secret']
    }

    res = call_api(url=url, headers=headers, params=request_params, request=Request.POST)
    
    return res['access_token']

def format_amadeus_data(res_api: dict, param_lat: float, param_long: float) -> pd.DataFrame:
    df = pd.DataFrame(res_api['data'], columns=['name','category','geoCode','rank','tags'])
    df = pd.concat([df.drop(['geoCode'], axis=1),df['geoCode'].apply(pd.Series)], axis=1)

    df['distance'] = df.apply(lambda x: relative_distance(lat1=param_lat, lon1=param_long, lat2=x.latitude, lon2=x.longitude), axis=1)

    df = df[['name','category','latitude','longitude','distance','rank','tags']]
    df = df.set_index('name')

    return df

def amadeus_pipeline(request_params: dict, isProd: bool = False):
    """
    Pipeline for the Amadeus API - Points of Interest
    """
    env_str = 'prod' if isProd else 'dev'

    config_path = f"{Path(__file__).resolve().parent}/config.json"

    with open(config_path,"r") as config_file:
        config = json.load(config_file)['amadeus_api'][env_str]

    auth_token = get_auth_token(config=config)

    url = config['poi_url']

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    res = call_api(url=url, headers=headers, params=request_params, request=Request.GET)

    activities_df = format_amadeus_data(res_api=res, param_lat=request_params['latitude'], param_long=request_params['longitude'])

    return activities_df
