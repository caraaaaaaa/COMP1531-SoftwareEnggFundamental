"""
This file is to test http for user_profile_setname function
function parameter: (token, name_first, name_last)
return: {}
"""

import urllib
import pytest
import requests
import json
from src import config


def test_http_user_profile_setname():
    """
    A simple test to check user_profile
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

    resp = requests.put(config.url + '/user/setname/v2', json={
        "token": owner.json()['token'],
        "name_first": "Eliza",
        "name_last": "Jones"
    })
    assert resp.status_code == 200


def test_user_profile_setfirstname_error():
    """
    test user_profile_setname input error
    first name is not 1-50 characters
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
    error1 = requests.get(config.url + '/user/setname/v2', json={
            "token": owner.json()['token'],
            "name_first": "Johnnnnnnnnohnnnnnnnnohnnnnnnnnohnnnnnnnnohnnnnnnnnnn",
            "name_last": "Smith",
        })
    assert error1.status_code == 405

    # with pytest.raises(urllib.error.HTTPError):
    error2 = requests.put(config.url + '/user/setname/v2', json={
            "token": owner.json()['token'],
            "name_first": "",
            "name_last": "Smith",
        })
    assert error2.status_code == 400


def test_user_profile_setlastname_error():
    """
    test user_profile_setname input error
    last name is not 1-50 characters
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
    error1 = requests.put(config.url + '/user/setname/v2', json={
            "token": owner.json()['token'],
            "name_first": "John",
            "name_last": "Smithnnnnnnnohnnnnnnnnohnnnnnnnnohnnnnnnnnohnnnnnnnnnn",
        })
    assert error1.status_code == 400

    # with pytest.raises(urllib.error.HTTPError):
    error2 = requests.put(config.url + '/user/setname/v2', json={
            "token": owner.json()['token'],
            "name_first": "John",
            "name_last": "",
        })
    assert error2.status_code == 400