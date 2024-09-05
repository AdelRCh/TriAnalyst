import requests
from dotenv import load_dotenv
import os
from typing import Optional, Union
import time
import datetime as dt

#Loading environment variables
load_dotenv()
WEATHER_API = os.getenv('WEATHER_API_KEY')

# Retrieving the information from our program requests:
def retrieve_event_coords(req_dump: requests.Response):
    '''Upon receiving Triathlon program data, we extract the date/time
    information as well as the latitude/longitude of the event.
    The output of this function is a dictionary with the keys "lat", "lon"
    and "dtime".'''

    # Sort the data
    req_data = req_dump.json()

    # Assembling the dictionary
    output = {
        "lat":req_data.get("event_latitude",None),
        "lon":req_data.get("event_longitude",None),
    }

    return output

def retrieve_date_info(req_dump: requests.Response):

    # Sort the data
    req_data = req_dump.json()

    # Get the date/time timestamp (in integer)
    dt_string = req_data.get("prog_date_utc",None) + "T"
    dt_string = dt_string + req_data.get("prog_time_utc",None) + "Z"
    prog_dt = dt.datetime.fromisoformat(dt_string).timestamp()

    return prog_dt

# Weather data request for a given timestamp.
def weather_history_request(lat, lon, dtime):
    '''This function returns weather data based on the latitude, longitude, and
    date/time in UTC. Upon receiving relevant information from the Triathlon
    API, we will forward them here for this API query.
    - lat: latitude, float
    - lon: longitude, float
    - dtime: date/timestamp in UTC, as an Integer input.
    Data is unavailable before Jan 1, 1979.'''
    global WEATHER_API
    api_url = 'https://history.openweathermap.org/data/3.0/history/timemachine'
    payload = {
        "lat":lat,
        "lon":lon,
        "dt":dtime,
        "appid": WEATHER_API
    }
    re = requests.get(url=api_url, params=payload)
    return re
