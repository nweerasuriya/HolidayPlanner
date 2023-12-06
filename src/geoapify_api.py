"""
Data Ingestion Script for Geoapify API

"""

__date__ = "2023-11-26"
__author__ = "NedeeshaWeerasuriya"
__version__ = "0.1"


# %% --------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.methods.data_ingestion import call_api
from src.helpers.utils import check_substr_in_dict

# %% --------------------------------------------------------------------------
# Main Script
# -----------------------------------------------------------------------------
def default_parameters() -> dict:
    """
    Default parameters for the Geoapify API
    """
    request_params = {
        "apiKey": "493bbfea1f124b27906cf052aa330680",
        "categories": "entertainment,tourism, leisure",
        "limit": "500",
    }
    return request_params


def create_url(url: str, request_params: dict, filters: dict) -> str:
    """
    Create URL for the Geoapify API
    """
    # append parameters to the url
    for key, value in request_params.items():
        url = url.replace("?", f"?{key}={value}&")

    # append filters to the url
    for key, value in filters.items():
        url = url.replace("?", f"?filter={key}:{value}&")

    # remove the last '&' from the url
    url = url[:-1]
    return url


def format_to_df(data: dict) -> pd.DataFrame:
    """
    Format and clean the data to a pandas dataframe
    """
    feature_list = []
    for i in range(len(data["features"])):
        # append rows to df
        feature_list.append(
            pd.DataFrame.from_dict(data["features"][i]["properties"], orient="index").T
        )

    # Combine into single dataframe
    df = pd.concat(feature_list, ignore_index=True)

    # expand datasource column into multiple columns
    df = pd.concat(
        [
            df.drop(["datasource", "place_id"], axis=1),
            df["datasource"].apply(pd.Series),
        ],
        axis=1,
    )

    # get website from dictionary in raw column if key containing sub string 'website' exists
    df['website'] = df['raw'].apply(lambda x: check_substr_in_dict(x, 'website'))

    # drop duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    # if name is not available, drop the row
    df = df.dropna(subset=["name"])

    # drop rows with identical names or postcodes
    df = df.drop_duplicates(subset=["name", "postcode"])
    # drop unnecessary columns
    df = df.drop(["raw","sourcename","details","attribution"], axis=1)
    # drop columns with nan rate over 90%
    df = df.dropna(thresh=len(df) * 0.1, axis=1)
    return df


def get_unique_words(cat_list) -> list:
    """
    Get unique words from the category list
    """
    unique_categories = []
    for category in cat_list:
        # Skip nan values
        if isinstance(category, str):
            # separate full stops ans spaces into separate words
            categories = category.split(".")
            categories = [category.split(" ") for category in categories]
            # flatten the list
            categories = [item for sublist in categories for item in sublist]
            unique_categories.append(categories)

    unique_categories = [item for sublist in unique_categories for item in sublist]
    unique_categories = list(set(unique_categories))
    return unique_categories


def geoapify_pipeline(url: str, request_params: dict, filters: dict) -> tuple:
    """
    Pipeline for the Geoapify API
    """
    # set default parameters if not provided
    if request_params == None:
        request_params = default_parameters()

    # create url
    url = create_url(url, request_params, filters)

    # call api
    data = call_api(url)

    # format data to df
    df = format_to_df(data)

    # get unique categories
    category_dict = {}
    for _, row in df.iterrows():
        category_dict[row["name"]] = get_unique_words(row["categories"])

    # join with df on name column
    df = df.drop(["categories"], axis=1).join(
        pd.Series(category_dict, name="category_keywords"), on="name"
    )
    return df, data