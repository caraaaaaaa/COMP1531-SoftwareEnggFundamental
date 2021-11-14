import pytest
import json
import requests
from src import config

def test_dm_list():
    #test for basic functionality
    #clear
    assert requests.delete(config.url+'clear/v1').status_code == 200
    
    #register owner1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'one@gmail.com',
        'password': 'pass123',
        'name_first': 'one',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    owner1 = resp.json()
    
    #register owner2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'two@gmail.com',
        'password': 'pass123',
        'name_first': 'two',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    owner2 = resp.json()
    
    #creating dm1 with owner1
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [],
    })
    assert resp.status_code == 200

    #creating dm2 with owner1
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [],
    })
    assert resp.status_code == 200
    
    #creating dm3 with owner1
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [],
    })
    assert resp.status_code == 200
    
    #viewing dm list for owner1
    resp = requests.get(config.url + 'dm/list/v1', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    dm_list = resp.json()
    
    assert len(dm_list['dms']) == 3
    
    #creating dm4 with owner2
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner2['token'],
        'u_ids': [],
    })
    assert resp.status_code == 200
    
    assert len(dm_list['dms']) == 3
    
    #viewing dm list for owner2
    resp = requests.get(config.url + 'dm/list/v1', json={
        'token': owner2['token'],
    })
    assert resp.status_code == 200
    dm_list = resp.json()
    
    assert len(dm_list['dms']) == 1
    
def test_dm_list_invalid_token():
    #test for invalid token
    #clear
    assert requests.delete(config.url+'clear/v1').status_code == 200
    
    #register owner1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'one@gmail.com',
        'password': 'pass123',
        'name_first': 'one',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    owner1 = resp.json()
    
    #register nonmember1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'two@gmail.com',
        'password': 'pass123',
        'name_first': 'two',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    
    #create dm1
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [],
    })
    assert resp.status_code == 200
    
    #view dm list with invalid token
    resp = requests.get(config.url+'dm/list/v1', json={
        'token': 0,
    })
    assert resp.status_code == 403

    #view dm list with invalid token
    resp = requests.get(config.url+'dm/list/v1', json={
        'token': {},
    })
    assert resp.status_code == 403
