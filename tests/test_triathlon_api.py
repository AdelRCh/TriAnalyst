import requests
import pytest
from dotenv import load_dotenv
import os

#Loading other directories within the project
import sys
sys.path.append('../')

from TriAnalyst.data_acquisition import triathlon_data as tri_data

PAUSE_NEEDED = False

def test_api_authentication():
    '''Testing the default query from the Triathlon API documentation'''
    global PAUSE_NEEDED
    tri_data.pause_between_reqs(PAUSE_NEEDED)
    qct = {"athlete_id":5895}
    re = tri_data.triathlon_api_request(section="athletes",
                                       query_content=qct, version="v1")
    PAUSE_NEEDED = True
    assert re.status_code==200

def test_events_endpoint():
    '''Testing whether the events endpoints work as they need to.'''
    global PAUSE_NEEDED
    tri_data.pause_between_reqs(PAUSE_NEEDED)
    qct={
        "per_page":10,
        "category_id":351,
        "order":"asc",
        "start_date":"2015-01-01",
        "end_date":"2016-01-01"
    }
    re = tri_data.triathlon_api_request(section="events",
                                       query_content=qct, version="v1")
    PAUSE_NEEDED = True
    assert re.status_code==200

def test_athlete_profile_retrieval():
    '''Testing whether we can retrieve an athlete's profile successfully'''
    global PAUSE_NEEDED
    tri_data.pause_between_reqs(PAUSE_NEEDED)
    qct={"output":"basic"}
    athlete_id=80795
    re = tri_data.triathlon_api_request(section="athletes",
                                        sub_argument=athlete_id,
                                        query_content=qct, version="v1")
    PAUSE_NEEDED = True
    assert re.status_code==200

def test_event_info_retrieval():
    '''Testing whether we can retrieve an event's information successfully'''
    global PAUSE_NEEDED
    tri_data.pause_between_reqs(PAUSE_NEEDED)
    event_id=90162
    re = tri_data.triathlon_api_request(section="events",
                                        sub_argument=event_id,
                                        version="v1")
    PAUSE_NEEDED = True
    assert re.status_code==200
