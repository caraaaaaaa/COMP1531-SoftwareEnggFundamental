import urllib
import pytest
import requests
import json
from src import config


def http_user_stats_v1():
    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    resp = requests.get(config.url + '/user/stats/v1', json={
        "token": owner.json()['token']
    })

    assert resp.status_code == 200


def http_user_profile_uploadphoto_v1():
    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    resp = requests.get(config.url + '/use/profile/uploadphoto/v1', json={
        "token": owner.json()['token'],
        "img_url": owner.json()['img_url'],
        "x_start": owner.json()['x_start'],
        "y_start": owner.json()['y_start'],
        "x_end": owner.json()['x_end'],
        "y_end": owner.json()['y_end']
    })

    assert resp.status_code == 200
