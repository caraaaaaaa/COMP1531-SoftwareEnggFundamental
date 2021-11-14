import pytest
import requests
import json
from src import config

# HTTP tests for /search/v2 and /clear/v1 routes

def test_search_v2():
    #Test basic functionality of search
    #clear
    assert requests.delete(config.url+'clear/v1').status_code == 200
    
    #register user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'benji@gmail.com',
        'password': 'pass123',
        'name_first': 'Benji',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    owner = resp.json()
    
    #register member
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'one@gmail.com',
        'password': 'pass123',
        'name_first': 'Benji',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    member = resp.json()
    
    #create dm
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member['auth_user_id']],
    })
    assert resp.status_code == 200
    dm = resp.json()
    
    #send dm message
    msgString1 = 'hey, how have you been lately?'
    resp = requests.post(config.url+'message/senddm/v1', json={
      'token': owner['token'],
      'dm_id': dm['dm_id'],
      'message': msgString1,
    })
    assert resp.status_code == 200
    
    #create channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': owner['token'],
        'name': 'mychannel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()
    
    #send message to channel
    msgString2 = 'I hope you have been enjoying yourself'
    resp = requests.post(config.url+'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'message': msgString2,
    })
    
    #use search
    query_str = 'have'
    resp = requests.get(config.url+'search/v2', json={
        'token': owner['token'],
        'query_str': query_str,
    })
    assert resp.status_code == 200
    results = resp.json()
    assert len(results['messages']) == 2
    
    #Test for input error when query string is more than 1000 characters
    #use search again
    query_str = ''
    counter = 0
    while counter < 1001:
        query_str += str(1)
        counter += 1
    assert len(query_str) == 1001
    resp = requests.get(config.url+'search/v2', json={
        'token': owner['token'],
        'query_str': query_str,
    })
    assert resp.status_code == 400
    
    #Test that the query string works when 1000 characters in length
    #use search again
    query_str = ''
    counter = 0
    while counter < 1000:
        query_str += str(1)
        counter += 1
    assert len(query_str) == 1000
    resp = requests.get(config.url+'search/v2', json={
        'token': owner['token'],
        'query_str': query_str,
    })
    assert resp.status_code == 200
    results = resp.json()
    assert len(results['messages']) == 0

    
    #Test for invalid token
    #clear
    assert requests.delete(config.url+'clear/v1').status_code == 200
    
    #use search
    resp = requests.get(config.url+'search/v2', json={
        'token': {},
        'query_str': '',
    })
    assert resp.status_code == 403
    
    #use search again
    resp = requests.get(config.url+'search/v2', json={
        'token': 0,
        'query_str': '',
    })
    assert resp.status_code == 403
    
def test_clear():
    #clear all users
    #clear
    assert requests.delete(config.url+'clear/v1').status_code == 200
    
    #register user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'one@gmail.com',
        'password': 'pass123',
        'name_first': 'one',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    owner = resp.json()
    
    #register user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'two@gmail.com',
        'password': 'pass123',
        'name_first': 'two',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    
    #register user3
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'three@gmail.com',
        'password': 'pass123',
        'name_first': 'three',
        'name_last': 'Kim',
    })
    
    #create channel1
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': owner['token'],
        'name': 'mychannel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    
    #create channel2
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': owner['token'],
        'name': 'mychannel2',
        'is_public': True,
    })
    assert resp.status_code == 200
    
    #create channel3
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': owner['token'],
        'name': 'mychannel3',
        'is_public': True,
    })
    assert resp.status_code == 200
    
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [],
    })
    assert resp.status_code == 200
    #create dm1
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [],
    })
    assert resp.status_code == 200

    #clear
    assert requests.delete(config.url+'clear/v1').status_code == 200
    
    #register user1 again
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'one@gmail.com',
        'password': 'pass123',
        'name_first': 'one',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    user = resp.json()
    
    #call all user information
    resp = requests.get(config.url + 'users/all/v1', json={
        'token': user['token'],  
    })
    assert resp.status_code == 200
    result = resp.json()
    assert len(result['users']) == 1

    #list all channels user is in
    resp = requests.get(config.url + 'channels/listall/v2', json={
        'token': user['token'],
    })
    assert resp.status_code == 200
    result = resp.json()
    assert len(result['channels']) == 0
    
    #list dm the user is in
    resp = requests.get(config.url + 'dm/list/v1', json={
        'token': user['token'],
    })
    
    assert resp.status_code == 200
    result = resp.json()
    assert len(result['dms']) == 0
    
