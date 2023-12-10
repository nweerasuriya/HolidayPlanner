"""
Utilities for the project
"""

__date__ = "2023-11-10"
__author__ = "NedeeshaWeerasuriya"

import os

import numpy as np


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
