import pytest
import json
import requests
from src import config

def test_dm_remove():
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
    
    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'two@gmail.com',
        'password': 'pass123',
        'name_first': 'two',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    member1 = resp.json()
    
    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [member1['auth_user_id']],
    })
    assert resp.status_code == 200
    dm = resp.json()
    
    #leave dm1
    resp = requests.delete(config.url + 'dm/remove/v1', json={
        'token': owner1['token'],
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 200
    leave_dm = resp.json()
    assert leave_dm == {}
    
    #list dm
    resp = requests.get(config.url + 'dm/list/v1', json={
        'token': owner1['token']
    })
    assert resp.status_code == 200
    dm_list = resp.json()
    
    assert len(dm_list['dms']) == 0

def test_dm_remove_invalid_token():
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
    
    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'two@gmail.com',
        'password': 'pass123',
        'name_first': 'two',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    member1 = resp.json()
    
    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [member1['auth_user_id']],
    })
    assert resp.status_code == 200
    dm = resp.json()
    
    #leave dm1 with invalid token 
    resp = requests.delete(config.url + 'dm/remove/v1', json={
        'token': 0,
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 403

    #leave dm1 with invalid token
    resp = requests.delete(config.url + 'dm/remove/v1', json={
        'token': {},
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 403
    
    #leave dm1 with invalid token
    resp = requests.delete(config.url + 'dm/remove/v1', json={
        'token': member1['token'],
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 403
    
    
    
