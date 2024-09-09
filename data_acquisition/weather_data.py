import requests
from dotenv import load_dotenv
import os
from typing import Optional, Union
import time
import datetime as dt

#Loading environment variables
load_dotenv()
WEATHER_API_OWD = os.getenv('WEATHER_API_KEY_OWD')
WEATHER_API_VC = os.getenv('WEATHER_API_KEY_VC')

# Retrieving the information from our program requests:
def retrieve_event_coords(event_data: dict):
    '''Upon receiving Triathlon event data, we extract the latitude/longitude
    of the event.

    Input:
    - event_data: a dictionary, the output of requests.Response.json()

    Returns:
    - a dictionary with {"lat":<value>, "lon":<value>} key-value pairs.'''

    # Assembling the dictionary
    output = {
        "lat":event_data.get("event_latitude",None),
        "lon":event_data.get("event_longitude",None),
    }

    return output

def retrieve_date_info(prog_data: dict):
    '''Upon receiving Triathlon program data, we extract the date/times in UTC
    and retrieve a Unix timestamp to forward to the Weather API.

    Input:
    - prog_data: a dictionary resulting from requests.Response.json()

    Returns:
    - a Unix timestamp (int type)'''

    # Get the date/time timestamp (in integer)
    dt_string = prog_data.get("prog_date_utc",'') + "T"

    # Force UTC, but keep backwards compatibility with old Python versions
    # (no Z, use +00:00 instead)
    dt_string = dt_string + prog_data.get("prog_time_utc",'') + "+00:00"
    prog_dt = dt.datetime.fromisoformat(dt_string).timestamp()

    return int(round(prog_dt))

# Weather data request for a given timestamp.
def weather_history_request_owm(coords:dict, dtime: int):
    '''This function returns weather data based on the latitude, longitude, and
    date/time in UTC from the OpenWeatherMap API. Upon receiving relevant
    information from the Triathlon API, we will use them for this query.
    - coords: the dictionary, output from retrieve_data_info()
    - dtime: date/timestamp in UTC, as an Integer input.
    Data is unavailable before Jan 1, 1979.'''
    global WEATHER_API_OWD
    api_url = 'https://history.openweathermap.org/data/3.0/history/timemachine'
    payload = {
        "lat":coords['lat'],
        "lon":coords['lon'],
        "dt":dtime,
        "appid": WEATHER_API_OWD
    }
    re = requests.get(url=api_url, params=payload)
    return re

def weather_history_request_vc(coords:dict, dtime: int):
    '''This function returns weather data based on the latitude, longitude, and
    date/time in UTC from the Visual Crossing API. Upon receiving relevant
    information from the Triathlon API, we will use them for this query.
    - coords: the dictionary, output from retrieve_data_info()
    - dtime: date/timestamp in UTC, as an Integer input.
    The data available covers a 50-year span..'''
    global WEATHER_API_VC
    api_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/'
    api_url = api_url + 'rest/services/timeline/'
    endpoint = f"{coords['lat']},{coords['lon']}/{dtime}"
    payload = {
        "key": WEATHER_API_VC,
        "unitGroup":"metric",
        "include": "current"
    }
    re = requests.get(url=api_url+endpoint, params=payload)
    return re
