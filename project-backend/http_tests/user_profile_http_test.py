"""
This file is to test http for user_profile function
function parameter: (token, u_id)
return: { user }
"""

import urllib

import pytest
import requests
import json
from src import config


def test_http_user_profile():
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

    resp = requests.get(config.url + '/user/profile/v2', json={
        "token": owner.json()['token'],
        "u_id": owner.json()['auth_user_id']
    })

    assert resp.status_code == 200


def test_user_profile_uiderror():
    """
    test user_profile input error
    u_id not valid
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
    error = requests.get(config.url + '/user/profile/v2', json={
            "token": owner.json()['token'],
            "u_id": "invalid u_id"
        })
    assert error.status_code == 400
