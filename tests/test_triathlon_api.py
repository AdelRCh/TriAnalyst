import requests
import pytest
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')

TRIATHLON_API = os.getenv('TRIATHLON_API_KEY')

def triathlon_api_request(section:str, query_content:dict,
                          filters:dict=None, version:str = "v1"):
    global TRIATHLON_API
    api_url="https://api.triathlon.org"
    re_url=f"{api_url}/{version}/{section}"
    re_headers = {'apikey': TRIATHLON_API}
    re = requests.get(url=re_url, headers=re_headers, params=query_content)
    return re

def test_api_authentication():
    '''Testing the default query from the Triathlon API documentation'''
    qct = {"athlete_id":5895}
    re = triathlon_api_request(section="athletes",query_content=qct,version="v1")
    assert re.status_code==200
