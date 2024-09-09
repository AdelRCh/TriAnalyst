import requests
import pytest
from dotenv import load_dotenv
import os

#Loading other directories within the project
import sys
sys.path.append('../')

from TriAnalyst.data_acquisition import triathlon_data as tri_data
from TriAnalyst.data_acquisition import weather_data as w_data
from TriAnalyst.data_acquisition import common_func as func

PAUSE_NEEDED = False
COORDS = {}
TIMESTAMP = 0

def test_api_authentication():
    '''Testing the default query from the Triathlon API documentation'''
    global PAUSE_NEEDED
    func.pause_between_reqs(PAUSE_NEEDED)
    qct = {"athlete_id":5895}
    re = tri_data.triathlon_api_request(section="athletes",
                                       query_content=qct, version="v1")
    PAUSE_NEEDED = True
    assert re.status_code==200

def test_events_endpoint():
    '''Testing whether the events endpoints work as they need to.'''
    global PAUSE_NEEDED
    func.pause_between_reqs(PAUSE_NEEDED)
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
    func.pause_between_reqs(PAUSE_NEEDED)
    qct={"output":"basic"}
    athlete_id=80795
    re = tri_data.triathlon_api_request(section="athletes",
                                        sub_args=athlete_id,
                                        query_content=qct, version="v1")
    PAUSE_NEEDED = True
    output = re.json().get("data",{}).get("athlete_title",'')
    assert re.status_code==200
    assert output=="Matthew Hauser"

def test_event_info_retrieval():
    '''Testing whether we can retrieve an event's information successfully'''
    global PAUSE_NEEDED
    global COORDS
    func.pause_between_reqs(PAUSE_NEEDED)
    event_id=90162
    re = tri_data.triathlon_api_request(section="events",
                                        sub_args=event_id,
                                        version="v1")
    PAUSE_NEEDED = True
    COORDS = w_data.retrieve_event_coords(re.json().get("data",{}))
    assert re.status_code==200
    assert COORDS != {}

def test_program_info_retrieval():
    '''Testing whether we can extract a program's info from an event'''
    global PAUSE_NEEDED
    global TIMESTAMP
    func.pause_between_reqs(PAUSE_NEEDED)
    event_id=90162
    #To note: booleans will instead be lowercase transcriptions of themselves.
    qct = {"is_race":"true"}

    re = tri_data.triathlon_api_request(section="events",
                                        sub_args=[event_id,"programs"],
                                        query_content=qct, version="v1")
    PAUSE_NEEDED = True
    TIMESTAMP = w_data.retrieve_date_info(re.json().get("data",[])[0])
    assert re.status_code==200
    assert TIMESTAMP!=0 #We have retrieved a timestamp

def test_weather_api_functionality_visualcrossing():
    '''Testing whether we have an output from our API with specific
    date/time/locations as input values'''
    global TIMESTAMP
    global COORDS
    re = w_data.weather_history_request_vc(coords=COORDS,dtime=TIMESTAMP)
    assert re.status_code==200
