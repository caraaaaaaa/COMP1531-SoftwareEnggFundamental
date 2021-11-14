import pytest
from src import config
import requests
import json
from time import sleep
from src.standup import time_finder
from datetime import datetime
from tests.standup_test import message_generator

'''PYTEST FIXTURES'''
@pytest.fixture
def user1():
    assert requests.delete(config.url+'clear/v1').status_code == 200
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'one@gmail.com',
        'password': 'pass123',
        'name_first': 'one',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    return resp.json()
    
@pytest.fixture
def user2():
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'two@gmail.com',
        'password': 'pass123',
        'name_first': 'two',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    return resp.json()

@pytest.fixture
def user3():
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'three@gmail.com',
        'password': 'pass123',
        'name_first': 'three',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    return resp.json()

def test_basic_standup_start_v1(user1):
    '''Test basic functionality of standup'''
    #create channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()
    
    #start standup
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    assert resp.status_code == 200
    standup = resp.json()
    
    #check output
    assert len(standup) == 1

def test_start_invalid_token(user1, user2, user3):
    '''Test for invalid token'''
    #create channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()
    
    #start standup with invalid token
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    
    assert resp.status_code == 403
    
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user3['token'],
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    
    assert resp.status_code == 403
    
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': 0,
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    
    assert resp.status_code == 403
    
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': {},
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    
    assert resp.status_code == 403
    
def test_start_invalid_channel_id(user1):
    '''Test for invalid channel id'''
    #create a channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    
    #start standup with invalid channel id
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': 'wrong',
        'length': 5,
    })
    
    assert resp.status_code == 400
    
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': {},
        'length': 5,
    })
    
    assert resp.status_code == 400
    
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': 0,
        'length': 5,
    })
    
    assert resp.status_code == 400

def test_start_already_active_standup(user1):
    '''Test when a standup is already in session'''
    #create channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()
    
    #start standup
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    assert resp.status_code == 200
    
    #starting standup while a standup is already in session
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    assert resp.status_code == 400

def test_standup_active_v1(user1):
    '''Test basic functionality of standup active'''
    #create channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()
    
    #get standup status 
    resp = requests.get(config.url+'standup/active/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
    })
    
    assert resp.status_code == 200
    status = resp.json()
    
    assert status == {
        'is_active': False,
        'time_finish': None,
    }
    
    #start a standup and check status_code
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    assert resp.status_code == 200

    resp = requests.get(config.url+'standup/active/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
    })
    
    assert resp.status_code == 200
    status = resp.json()
    assert status['is_active'] == True
    assert isinstance(status['time_finish'], int) == True

def test_active_invalid_token(user1, user2, user3):
    '''Test for invalid token'''
    #create a channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()

    #check if standup is active with invalid token
    resp = requests.get(config.url+'standup/active/v1', json={
        'token': user2['token'],
        'channel_id': channel['channel_id'],
    })
    
    assert resp.status_code == 403
    
    resp = requests.get(config.url+'standup/active/v1', json={
        'token': user3['token'],
        'channel_id': channel['channel_id'],
    })
    
    assert resp.status_code == 403
    
    resp = requests.get(config.url+'standup/active/v1', json={
        'token': 0,
        'channel_id': channel['channel_id'],
    })
    
    assert resp.status_code == 403
    
    resp = requests.get(config.url+'standup/active/v1', json={
        'token': {},
        'channel_id': channel['channel_id'],
    })
    
    assert resp.status_code == 403

def test_active_invalid_channel(user1):
    '''Test for invalid channel id'''
    #create a channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200

    #check if standup is active with invalid channel id
    resp = requests.get(config.url+'standup/active/v1', json={
        'token': user1['token'],
        'channel_id': 0,
    })
    
    assert resp.status_code == 400
    
    resp = requests.get(config.url+'standup/active/v1', json={
        'token': user1['token'],
        'channel_id': {},
    })
    
    assert resp.status_code == 400
    
    resp = requests.get(config.url+'standup/active/v1', json={
        'token': user1['token'],
        'channel_id': 'wrong',
    })
    
    assert resp.status_code == 400

def test_standup_send_v1(user1, user2, user3):
    '''Test basic functionality of startup send'''
    #create a channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()
    
    #invite user2
    resp = requests.post(config.url+'channel/invite/v2', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user2['auth_user_id'],
    })
    assert resp.status_code == 200

    #invite user3
    resp = requests.post(config.url+'channel/invite/v2', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user3['auth_user_id'],
    })
    assert resp.status_code == 200
    
    #start standup
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    assert resp.status_code == 200
    
    #user1 send message to standup
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'message': 'hello',
    })
    assert resp.status_code == 200
    standup = resp.json()
    
    assert standup == {}
    
    #user2 send message to standup
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'message': 'hello',
    })
    assert resp.status_code == 200

    #user3 send message to standup
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': user3['token'],
        'channel_id': channel['channel_id'],
        'message': 'hello',
    })
    assert resp.status_code == 200
    sleep(5)

    #check if messages were collated together and sent to the messages key
    resp = requests.get(config.url+'channel/messages/v2', json={
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'start': 0,
    })
    assert resp.status_code == 200
    messages = resp.json()
    
    assert messages['messages'][0]['message'] == 'one: hello\n'+'two: hello\n'+'three: hello'
    
def test_send_invalid_token(user1, user2, user3):
    '''Test for invalid token'''
    #create a channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()

    #start standup
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    assert resp.status_code == 200
    
    #send messages to standup using invalid token
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'message': 'hello',
    })
    assert resp.status_code == 403

    resp = requests.post(config.url+'standup/send/v1', json={
        'token': user3['token'],
        'channel_id': channel['channel_id'],
        'message': 'hello',
    })
    assert resp.status_code == 403
    
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': 0,
        'channel_id': channel['channel_id'],
        'message': 'hello',
    })
    assert resp.status_code == 403
    
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': {},
        'channel_id': channel['channel_id'],
        'message': 'hello',
    })
    assert resp.status_code == 403

def test_send_invalid_channel_id(user1):
    '''Test for invalid channel id'''
    #create a channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()
    
    #start standup
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    assert resp.status_code == 200
    
    #send message with invalid channel id
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': user1['token'],
        'channel_id': 0,
        'message': 'hello',
    })
    assert resp.status_code == 400

    resp = requests.post(config.url+'standup/send/v1', json={
        'token': user1['token'],
        'channel_id': '1',
        'message': 'hello',
    })
    assert resp.status_code == 400
    
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': user1['token'],
        'channel_id': {},
        'message': 'hello',
    })
    assert resp.status_code == 400
    
def test_send_invalid_message(user1):
    '''Test for invalid message'''
    #create a channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()
    
    #start standup
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    assert resp.status_code == 200
    
    #send 1000 character message
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'message': message_generator(1000),
    })
    assert resp.status_code == 200
    
    #send 1001 character message
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'message': message_generator(1001),
    })
    assert resp.status_code == 400

def test_send_standup_inactive(user1):
    '''Test for when a standup is not active'''
    #create a channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    
    #send message to inactive standup
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': user1['token'],
        'channel_id': '1',
        'message': 'hello',
    })
    assert resp.status_code == 400
