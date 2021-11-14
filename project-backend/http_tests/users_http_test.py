"""
This file is to test http for channel_join_v2 function
function parameter: (token, channel_id)
return: {}
"""

import urllib
import pytest
import requests
import json
from src import config


def test_http_users_all():
    """
    A simple test to check users all
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

    user = requests.post(config.url + 'auth/register/v2', json={
        "email": "eliza.jones2@gmail.com",
        "password": "pass123",
        "name_first": "Eliza",
        "name_last": "Jones"
    })
    assert user.status_code == 200

    resp = requests.get(config.url + '/users/all/v1', json={
        "token": owner.json()['token'],
    })
    assert resp.status_code == 200


def http_users_stats_v1():
    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    resp = requests.get(config.url + '/users/stats/v1', json={
        "token": owner.json()['token']
    })

    assert resp.status_code == 200
