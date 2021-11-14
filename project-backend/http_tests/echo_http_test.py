import pytest
import requests
from src import config
from json import loads, dumps
from src.error import InputError

def test_echo():
    '''
    A simple test to check echo
    '''
    resp = requests.get(config.url + 'echo', params={'data': 'hello'})
    payload = resp.json()
    assert payload == {'data': 'hello'}
