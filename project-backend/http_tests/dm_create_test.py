import pytest
import json
import requests 
from src import config

def test_dm_create():
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
    #creating dm1
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [member1['auth_user_id']],
    })
    assert resp.status_code == 200
    dm1 = resp.json()
    
    #viewing dm1 details
    resp = requests.get(config.url+'dm/details/v1', json={
        'token': owner1['token'],
        'dm_id': dm1['dm_id'],
    })
    assert resp.status_code == 200
    details = resp.json()
    
    assert len(details['members']) == 2
    assert details['name'] == "one.last#1,two.last#2"
    
    #creating dm2
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']],
    })
    assert resp.status_code == 200
    dm2 = resp.json()
    
    #viewing dm2 details
    resp = requests.get(config.url+'dm/details/v1', json={
        'token': owner1['token'],
        'dm_id': dm2['dm_id'],
    })
    assert resp.status_code == 200
    details = resp.json()
    
    assert len(details['members']) == 3
    assert details['name'] == "one.last#1,three.last#3,two.last#2"

def test_dm_create_invalid_token():
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
    
    #creating dm with invalid token 
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': 0,
        'u_ids': [],
    })
    assert resp.status_code == 403
    
    #creating dm with invalid token 
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': {},
        'u_ids': [],
    })
    assert resp.status_code == 403
    
    #creating dm with invalid token 
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': '1234556',
        'u_ids': [],
    })
    assert resp.status_code == 403
    
def test_dm_create_uids():
    
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
        
    #creating dm with u_ids
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': 'hello',
    })
    assert resp.status_code == 400
    
    #creating dm with u_ids
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': 0,
    })
    assert resp.status_code == 400
    
    #creating dm with u_ids
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': {},
    })
    assert resp.status_code == 400
    
    #creating dm with u_ids
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [owner1['auth_user_id']],
    })
    assert resp.status_code == 400

