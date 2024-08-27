import requests
from dotenv import load_dotenv
import os
from typing import Optional, Union
import time

#Loading environment variables
load_dotenv()
TRIATHLON_API = os.getenv('TRIATHLON_API_KEY')
WEATHER_API = os.getenv('WEATHER_API_KEY')

# General API request function template (fit for purpose)
def triathlon_api_request(section:str, query_content:dict={},
                          sub_args:Optional[Union[int,str,list]]=None,
                          filters:dict=None, version:str = "v1"):
    '''The request function of our project for Triathlon API queries.
    Inputs:
    - section: the desired endpoint (athletes, events, programs, etc.)
    - sub_argument: an addition to the endpoint if needed (e.g.: athlete_id)
    - query_content: any valid query argument (check the API's documentation)
    - filters: only if needed
    - version: unless the Triathlon API releases an update, uses "v1" by default

    Returns:
    - A request's outcome (see requests.get() documentation)
    '''
    global TRIATHLON_API
    api_url="https://api.triathlon.org"
    re_url=f"{api_url}/{version}/{section}"

    # Sub-arguments if needed (e.g.: athletes/<athlete_id>?...)
    if sub_args is not None:
        #In the case of event programs (many triathlon categories in one event),
        #we will receive a list of parameters. We will then unwrap them as
        #param_1/param_2/param_3/.../param_n
        if isinstance(sub_args,list):
            sub_arg_str = '/'.join([f'{item}' for item in sub_args])
            api_url = api_url+f'/{sub_arg_str}'

        #Otherwise, we will likely only receive one argument.
        else:
            api_url=api_url+f'/{sub_args}'

    # Supplies the Triathlon API key to the request. Do not remove.
    re_headers = {'apikey': TRIATHLON_API}

    # If needed, supply filters for queries.
    if filters is not None:
        parsed_filters=''
        for key, value in filters.items():
            if parsed_filters is not None:
                parsed_filters = parsed_filters + '|'
            parsed_filters = parsed_filters + f'{key},{value}'
        query_content.append({"filters":parsed_filters})

    re = requests.get(url=re_url, headers=re_headers, params=query_content)
    return re

# Preventing the "Too Many Requests" error code, avoiding rate limitations.
def pause_between_reqs(needed:bool=False):
    if needed:
        time.sleep(10)
