"""
This file is to test http for user_profile_sethandle function
function parameter: (token, handle_str)
return: {}
"""

import urllib
import pytest
import requests
import json
from src import config


def test_http_user_profile_sethandle():
    """
    A simple test to check user_profile_sethandle
    """

    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    resp = requests.put(config.url + '/user/sethandle/v2', json={
        "token": owner.json()['token'],
        "handle_str": "newhandle"
    })
    assert resp.status_code == 200


def test_user_profile_setfirstname_error():
    """
    test user_profile_setname input error
    first name is not 3-20 characters
    """

    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    # with pytest.raises(urllib.error.HTTPError):
    error1 = requests.put(config.url + '/user/sethandle/v2', json={
            "token": owner.json()['token'],
            "handle_str": "jo"
        })
    assert error1.status_code == 400

    # with pytest.raises(urllib.error.HTTPError):
    error2 = requests.put(config.url + '/user/sethandle/v2', json={
            "token": owner.json()['token'],
            "handle_str": "joohnnnnnnnnohnnnnnnnnohnnnnnnnnohnnnnnnn"
        })
    assert error2.status_code == 400