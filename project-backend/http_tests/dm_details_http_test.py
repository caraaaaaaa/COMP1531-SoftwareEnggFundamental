import pytest
import json
import requests
from src import config

def test_dm_details_v1():
    #Test for basic functionality
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
    
    #register member2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'three@gmail.com',
        'password': 'pass123',
        'name_first': 'three',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    member2 = resp.json()
    
    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']],
    })
    assert resp.status_code == 200
    dm = resp.json()
    
    #view dm details
    resp = requests.get(config.url + 'dm/details/v1', json={
        'token': owner1['token'],
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 200
    details = resp.json()
    
    assert details['name'] == 'one.last#1,three.last#3,two.last#2'
    assert len(details['members']) == 3
    
def test_dm_details_invalid_token():
    #Test for invalid token
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
    nonmember1 = resp.json()
    
    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [],
    })
    assert resp.status_code == 200
    dm = resp.json()
    
    #view dm details with invalid token
    resp = requests.get(config.url + 'dm/details/v1', json={
        'token': 0,
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 403

    #view dm details with invalid token
    resp = requests.get(config.url + 'dm/details/v1', json={
        'token': {},
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 403
    
    #view dm details with invalid token
    resp = requests.get(config.url + 'dm/details/v1', json={
        'token': 'hello',
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 403
    
    #view dm details with invalid token
    resp = requests.get(config.url + 'dm/details/v1', json={
        'token': nonmember1['token'],
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 403

def test_dm_details_invalid_dm():
    #Test for invalid dm_id
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

    #view dm with invalid dm_id
    resp = requests.get(config.url+'dm/details/v1', json={
        'token': owner1['token'],
        'dm_id': 0,
    })
    assert resp.status_code == 400
    
    #view dm with invalid dm_id
    resp = requests.get(config.url+'dm/details/v1', json={
        'token': owner1['token'],
        'dm_id': {},
    })
    assert resp.status_code == 400
    
    #view dm with invalid dm_id
    resp = requests.get(config.url+'dm/details/v1', json={
        'token': owner1['token'],
        'dm_id': 'hello',
    })
    assert resp.status_code == 400
