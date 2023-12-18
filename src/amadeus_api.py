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
from src.methods.data_ingestion import call_api, Request


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

def amadeus_pipeline(request_params: dict, isProd: bool = False):
    """
    Pipeline for the Amadeus API - Points of Interest
    """
    env_str = 'prod' if isProd else 'dev'

    config_path = f"{Path(__file__).resolve().parent}\config.json"

    with open(config_path,"r") as config_file:
        config = json.load(config_file)['amadeus_api'][env_str]

    auth_token = get_auth_token(config=config)

    url = config['poi_url']

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    res = call_api(url=url, headers=headers, params=request_params, request=Request.GET)

    return res
