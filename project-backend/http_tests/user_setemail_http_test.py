"""
This file is to test http for user_profile_setemail function
function parameter: (token, email)
return: {}
"""

import urllib
import pytest
import requests
import json
from src import config


def test_http_user_profile_setemail():
    """
    A simple test to check user_profile_setemail
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

    resp = requests.put(config.url + '/user/setemail/v2', json={
        "token": owner.json()['token'],
        "email": "john.smith7@gmail.com"
    })
    assert resp.status_code == 200


def test_user_profile_set_invalidemail_error():
    """
    test user_profile_setemail input error
    new email is not valid email format
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
    error = requests.put(config.url + '/user/setemail/v2', json={
            "token": owner.json()['token'],
            "email": "john.smith8gmail.com",
        })
    assert error.status_code == 400


def test_user_profile_set_usedemail_error():
    """
    test user_profile_setemail input error
    new email being used by others
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

    user = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith5@gmail.com",
        "password": "pass123",
        "name_first": "Johnn",
        "name_last": "Smith",
    })
    assert user.status_code == 200

    # with pytest.raises(urllib.error.HTTPError):
    error = requests.put(config.url + '/user/setemail/v2', json={
            "token": owner.json()['token'],
            "email": "john.smith5@gmail.com",
        })
    assert error.status_code == 400
