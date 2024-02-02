"""
AccuWeather API wrapper for Python/asyncio.

For more details about this api, please refer to the documentation at https://developer.accuweather.com/apis
"""

__date__ = "2024-01-20"
__author__ = "NedeeshaWeerasuriya"
__version__ = "0.1"


import logging

from accuweather import (
    AccuWeather,
    ApiError,
    InvalidApiKeyError,
    InvalidCoordinatesError,
    RequestsExceededError,
)
from aiohttp import ClientError, ClientSession

logging.basicConfig(level=logging.DEBUG)

API_KEY = "82dnHOCuRLFezoSzY3ZlPd5D113lU4pJ"


async def main(lat, long):
    """Run main function."""
    async with ClientSession() as websession:
        try:
            accuweather = AccuWeather(
                API_KEY,
                websession,
                latitude=lat,
                longitude=long,
                language="pl",
            )
            current_conditions = await accuweather.async_get_current_conditions()
            forecast_daily = await accuweather.async_get_daily_forecast(
                days=5, metric=True
            )
            forecast_hourly = await accuweather.async_get_hourly_forecast(
                hours=12, metric=True
            )
        except (
            ApiError,
            InvalidApiKeyError,
            InvalidCoordinatesError,
            ClientError,
            RequestsExceededError,
        ) as error:
            print(f"Error: {error}")
        else:
            print(f"Location: {accuweather.location_name} ({accuweather.location_key})")
            print(f"Requests remaining: {accuweather.requests_remaining}")
            print(f"Current: {current_conditions}")
            print(f"Forecast: {forecast_daily}")
            print(f"Forecast hourly: {forecast_hourly}")
            return current_conditions, forecast_daily, forecast_hourly
