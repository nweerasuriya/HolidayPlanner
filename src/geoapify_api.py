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
from src.helpers.time_tracker import track_time

# %% --------------------------------------------------------------------------
# Main Script
# -----------------------------------------------------------------------------
def default_parameters() -> dict:
    """
    Default parameters for the Geoapify API
    """
    request_params = {
        "apiKey": str(input("Enter your API key: ")),
        "categories": "entertainment,tourism, leisure",
        "limit": "500",
    }
    return request_params


@track_time
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


@track_time
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

    # extract opening hours from dictionary in raw column if 'opening_hours' exists
    df["opening_hours"] = df["raw"].apply(
        lambda x: check_substr_in_dict(x, "opening_hours")
    )
    # get website from dictionary in raw column if key containing sub string 'website' exists
    df["website"] = df["raw"].apply(lambda x: check_substr_in_dict(x, "website"))

    # drop duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    # if name is not available, drop the row
    df = df.dropna(subset=["name"])

    # drop rows with identical names or postcodes
    df = df.drop_duplicates(subset=["name", "postcode"])
    # drop unnecessary columns
    df = df.drop(["raw", "url", "sourcename", "details", "attribution"], axis=1)

    # drop columns with nan rate over 90%
    df_filtered = df.dropna(thresh=len(df) * 0.1, axis=1)

    exclude_list = ["opening_hours", "website"]
    for col in exclude_list:
        if col in df.columns and col not in df_filtered.columns:
            df_filtered[col] = df[col]

    return df_filtered


@track_time
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


@track_time
def add_weather_tags(
    categories: list,
    outdoor_tags: list = None,
    indoor_tags: list = None,
    both_tags: list = None,
) -> int:
    """
    Add weather tags based on the category key words in a list
    Produce a score between 1 and 5 based on the number of outdoor, indoor and both tags
    5 indicates places should only be visited in good weather
    """
    if outdoor_tags == None:
        outdoor = [
            "park",
            "beach",
            "garden",
            "lake",
            "river",
            "mountain",
            "viewpoint",
            "bridge",
            "square",
            "archaeological_site",
            "monument",
        ]
    if indoor_tags == None:
        indoor = [
            "building",
            "cinema",
            "theatre",
            "museum",
            "gallery",
            "aquarium",
            "zoo",
            "library",
        ]
    if both_tags == None:
        both = ["castle", "ruins", "ruines", "university"]

    # outdoor tags are worth 5 points, both tags are worth 2 points, indoor tags are worth 0 points
    outdoor_count = 0
    indoor_count = 0
    both_count = 0
    for category in categories:
        if category in outdoor:
            outdoor_count += 1
        elif category in indoor:
            indoor_count += 1
        elif category in both:
            both_count += 1

    # if no tags are found, return 0
    if outdoor_count + both_count + indoor_count == 0:
        weather_tag = 3
    # calculate the weather tag
    else:
        # Scale the score between 1 and 5
        weather_tag = int(
            np.clip(
                (outdoor_count * 5 + both_count * 2)
                / (outdoor_count + both_count + indoor_count),
                1,
                5,
            )
        )
    return weather_tag


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

    # get unique categories and add weather tags
    category_dict = {}
    weather_tags = {}
    for _, row in df.iterrows():
        category_dict[row["name"]] = get_unique_words(row["categories"])
        weather_tags[row["name"]] = add_weather_tags(category_dict[row["name"]])

    # add categories and drop original column
    df = df.drop(["categories"], axis=1).join(
        pd.Series(category_dict, name="category_keywords"), on="name"
    )
    # add weather tags
    df["weather_tags"] = df["name"].map(weather_tags)

    return df, data
