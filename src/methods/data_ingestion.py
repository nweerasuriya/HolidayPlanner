"""
Data Ingestion Methods

Contains functions to ingest data from a file and format it
"""

__date__ = "2023-11-10"
__author__ = "NedeeshaWeerasuriya"
__version__ = "0.1"


import numpy as np
import pandas as pd
from src.helpers.time_tracker import track_time
from src.helpers.utils import is_number


@track_time
def format_data(df):
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
def filter_data_ranges(data, data_range):
    """
    Filter data based on specified ranges
    """
    # Filter lower values
    data = data.loc[data.values >= data_range[0]]
    # Filter upper values
    data = data.loc[data.values <= data_range[1]]

    return data