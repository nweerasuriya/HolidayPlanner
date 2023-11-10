"""
Utilities for the project

"""

__date__ = "2023-11-10"
__author__ = "NedeeshaWeerasuriya"

import os

def create_folder(directory):
    """
    create a given folder if fit does not exit
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
    return directory