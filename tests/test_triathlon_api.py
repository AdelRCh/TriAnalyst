import requests
import pytest
from dotenv import load_dotenv
import os

#Loading other directories within the project
import sys
sys.path.append('../')

from TriAnalyst.data_acquisition import triathlon_data as tri_data

def test_api_authentication():
    '''Testing the default query from the Triathlon API documentation'''
    qct = {"athlete_id":5895}
    re = tri_data.triathlon_api_request(section="athletes",
                                       query_content=qct, version="v1")
    assert re.status_code==200
