import requests
from dotenv import load_dotenv
import os

#Loading environment variables
load_dotenv()
TRIATHLON_API = os.getenv('TRIATHLON_API_KEY')
WEATHER_API = os.getenv('WEATHER_API_KEY')

# Template for an API request function
def triathlon_api_request(section:str, query_content:dict,
                          filters:dict=None, version:str = "v1"):
    global TRIATHLON_API
    api_url="https://api.triathlon.org"
    re_url=f"{api_url}/{version}/{section}"
    re_headers = {'apikey': TRIATHLON_API}
    re = requests.get(url=re_url, headers=re_headers, params=query_content)
    return re
