"""
Time tracker helper class to measure time spent in different functions.
"""

__date__ = "2023-11-10"
__author__ = "NedeeshaWeerasuriya"


import functools
import time
from typing import Any, Callable, Dict
import matplotlib.pyplot as plt
import pandas as pd

TIMINGS: Dict[str, float] = {}


def track_time(func: Callable) -> Callable:
    """Decorator that tracks the time a function takes to execute and stores it."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        TIMINGS[func.__name__] = TIMINGS.get(func.__name__, 0) + (end_time - start_time)
        return result

    return wrapper


def timings_to_dataframe() -> pd.DataFrame:
    """Returns a DataFrame with the function names and their respective timings."""
    return pd.DataFrame(list(TIMINGS.items()), columns=["Function", "Time"])


def plot_timings():
    """Plots the timing data."""
    names = list(TIMINGS.keys())
    times = list(TIMINGS.values())
    plt.bar(names, times)
    plt.xlabel("Function")
    plt.ylabel("Time (seconds)")
    plt.title("Function Execution Times")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()