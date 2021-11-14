import pytest
import requests
import json
from src import config
from datetime import datetime
from time import sleep


def test_message_send():

    #TEST BASIC FUNCTIONALLITY

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #obtain message contents
    resp = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = resp.json()
    assert resp.status_code == 200
    assert message_list['messages'][0]['message'] == "Hello World!"

    #TEST INPUT ERROR FOR MESSAGE LENGTH > 1000

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 1001*'h',
    })
    assert resp.status_code == 400

    #TEST ACCESS ERROR FOR INVALID USER

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register new user
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #user sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': user['token'],
        'channel_id': channel_id,
        'message': 1001*'h',
    })
    assert resp.status_code == 400

def test_message_edit():

    #TEST BASIC FUNCTIONALLITY

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #owner edits message
    resp = requests.put(config.url + 'message/edit/v2', json={
        'token': owner['token'],
        'message_id': m_id1,
        'message': 'Goodbye World...',
    })
    assert resp.status_code == 200

    #obtain message contents
    resp = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = resp.json()['messages'][0]['message']
    assert resp.status_code == 200
    assert message_list == "Goodbye World..."

    #TEST EDIT EMPTY

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #owner deletes message
    resp = requests.put(config.url + 'message/edit/v2', json={
        'token': owner['token'],
        'message_id': m_id1,
        'message': '',
    })
    assert resp.status_code == 200

    #obtain message contents
    resp = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'start': 0,
    })
    assert resp.status_code == 200
    message_list = resp.json()['messages']
    assert len(message_list) == 0


    #TEST INPUT ERROR FOR MESSAGE LENGTH > 1000

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #owner edits message
    resp = requests.put(config.url + 'message/edit/v2', json={
        'token': owner['token'],
        'message_id': m_id1,
        'message': 1001*'h',
    })
    assert resp.status_code == 400

    #TEST INPUT ERROR FOR EDITING DELETED MESSAGE

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #owner deletes message
    resp = requests.put(config.url + 'message/edit/v2', json={
        'token': owner['token'],
        'message_id': m_id1,
        'message': '',
    })
    assert resp.status_code == 200

    #owner edits message
    resp = requests.put(config.url + 'message/edit/v2', json={
        'token': owner['token'],
        'message_id': m_id1,
        'message': 'Yo!',
    })
    assert resp.status_code == 400

    #TEST ACCESS ERROR FOR INVALID USER

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register new user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register new user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Chau@gmail.com',
        'password': 'farmfiesta',
        'name_first': 'Poppy',
        'name_last': 'Chau',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #invite user 1
    resp = requests.post(config.url + 'channel/join/v2', json={
        'token': user1['token'],
        'channel_id': channel_id,
    })
    assert resp.status_code == 200

    #invite user 2
    resp = requests.post(config.url + 'channel/join/v2', json={
        'token': user2['token'],
        'channel_id': channel_id,
    })
    assert resp.status_code == 200

    #user1 sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': user1['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #owner edits message
    resp = requests.put(config.url + 'message/edit/v2', json={
        'token': owner['token'],
        'message_id': m_id1,
        'message': 'Hello Everyone!',
    })
    assert resp.status_code == 200

    #user2 edits message
    resp = requests.put(config.url + 'message/edit/v2', json={
        'token': user2['token'],
        'message_id': m_id1,
        'message': 'Yo!',
    })
    assert resp.status_code == 403

def test_message_remove():

    #TEST FOR NORMAL FUNCTIONALLITY

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #owner deletes message
    resp = requests.delete(config.url + 'message/remove/v1', json={
        'token': owner['token'],
        'message_id': m_id1,
    })
    assert resp.status_code == 200

    #obtain message contents
    resp = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'start': 0,
    })
    assert resp.status_code == 200
    message_list = resp.json()['messages']
    assert len(message_list) == 0
    #TEST FOR ALREADY DELETED MESSAGE

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #owner deletes message
    resp = requests.delete(config.url + 'message/remove/v1', json={
        'token': owner['token'],
        'message_id': m_id1,
    })
    assert resp.status_code == 200

    #owner deletes message again
    resp = requests.delete(config.url + 'message/remove/v1', json={
        'token': owner['token'],
        'message_id': m_id1,
    })
    assert resp.status_code == 400

    #TEST ACCESS ERROR FOR INVALID USER

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register new user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register new user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Chau@gmail.com',
        'password': 'farmfiesta',
        'name_first': 'Poppy',
        'name_last': 'Chau',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #invite user 1
    resp = requests.post(config.url + 'channel/join/v2', json={
        'token': user1['token'],
        'channel_id': channel_id,
    })
    assert resp.status_code == 200

    #invite user 2
    resp = requests.post(config.url + 'channel/join/v2', json={
        'token': user2['token'],
        'channel_id': channel_id,
    })
    assert resp.status_code == 200

    #user1 sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': user1['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #user2 deletes message
    resp = requests.delete(config.url + 'message/remove/v1', json={
        'token': user2['token'],
        'message_id': m_id1,
    })
    assert resp.status_code == 403

def test_message_share():

    #TEST BASIC FUNCTIONALLITY

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id1 = resp.json()['channel_id']

    #create channel2
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_Two',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id2 = resp.json()['channel_id']

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id1,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #owner shares message
    resp = requests.post(config.url + 'message/share/v1', json={
        'token': owner['token'],
        'og_message_id' : m_id1,
        'message': 'Wow!',
        'channel_id': channel_id2,
        'dm_id' : -1,
    })
    assert resp.status_code == 200

    #obtain message contents
    resp = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel_id2,
        'start': 0,
    })
    message_list = resp.json()['messages'][0]['message']
    assert resp.status_code == 200
    assert message_list == '"Hello World!"\nWow!'

    #TEST WITH NO ADDITIONAL MESSAGE

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id1 = resp.json()['channel_id']

    #create channel2
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_Two',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id2 = resp.json()['channel_id']

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id1,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #owner shares message
    resp = requests.post(config.url + 'message/share/v1', json={
        'token': owner['token'],
        'og_message_id' : m_id1,
        'message': '',
        'channel_id': channel_id2,
        'dm_id' : -1,
    })
    assert resp.status_code == 200

    #obtain message contents
    resp = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel_id2,
        'start': 0,
    })
    message_list = resp.json()['messages'][0]['message']
    assert resp.status_code == 200
    assert message_list == '"Hello World!"'

    #TEST ACCESS ERROR SHARING TO CHANNEL USER IS NOT APART OF

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner1 = resp.json()

    #register owner2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    owner2 = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id1 = resp.json()['channel_id']

    #create channel2
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner2['token'],
        'name': 'Channel_Two',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id2 = resp.json()['channel_id']

    #owner1 sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner1['token'],
        'channel_id': channel_id1,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #owner1 shares message
    resp = requests.post(config.url + 'message/share/v1', json={
        'token': owner1['token'],
        'og_message_id' : m_id1,
        'message': '',
        'channel_id': channel_id2,
        'dm_id' : -1,
    })
    assert resp.status_code == 403

    #TEST BASIC FUNCTIONALLITY WITH DM

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #register user3
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Chau@gmail.com',
        'password': 'farmfiesta',
        'name_first': 'Poppy',
        'name_last': 'Chau',
    })
    assert resp.status_code == 200
    user3 = resp.json()

    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id1 = resp.json()['dm_id']

    #create dm2
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user3['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id2 = resp.json()['dm_id']

    #user2 sends message
    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user2['token'],
        'dm_id': dm_id1,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #user1 shares message to user3
    resp = requests.post(config.url + 'message/share/v1', json={
        'token': user1['token'],
        'og_message_id' : m_id1,
        'message': 'Get a load of this guy!',
        'channel_id': -1,
        'dm_id' : dm_id2,
    })
    assert resp.status_code == 200

    #obtain message contents
    resp = requests.get(config.url + 'dm/messages/v1', json={
        'token': user1['token'],
        'dm_id': dm_id2,
        'start': 0,
    })
    assert resp.status_code == 200
    message_list = resp.json()
    assert message_list['messages'][0]['message'] == '"Hello World!"\nGet a load of this guy!'

    #TEST DM SHARE WITH NO ADDITIONAL MESSAGE

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #register user3
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Chau@gmail.com',
        'password': 'farmfiesta',
        'name_first': 'Poppy',
        'name_last': 'Chau',
    })
    assert resp.status_code == 200
    user3 = resp.json()

    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id1 = resp.json()['dm_id']

    #create dm2
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user3['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id2 = resp.json()['dm_id']

    #user2 sends message
    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user2['token'],
        'dm_id': dm_id1,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #user1 shares message to user3
    resp = requests.post(config.url + 'message/share/v1', json={
        'token': user1['token'],
        'og_message_id' : m_id1,
        'message': '',
        'channel_id': -1,
        'dm_id' : dm_id2,
    })
    assert resp.status_code == 200

    #obtain message contents
    resp = requests.get(config.url + 'dm/messages/v1', json={
        'token': user1['token'],
        'dm_id': dm_id2,
        'start': 0,
    })
    message_list = resp.json()['messages'][0]['message']
    assert resp.status_code == 200
    assert message_list == '"Hello World!"'

    #TEST DM SHARE ACCESS ERROR WHEN USER IS NOT APART OF DM

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #register user3
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Chau@gmail.com',
        'password': 'farmfiesta',
        'name_first': 'Poppy',
        'name_last': 'Chau',
    })
    assert resp.status_code == 200
    user3 = resp.json()

    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id1 = resp.json()['dm_id']

    #create dm2
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user3['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id2 = resp.json()['dm_id']

    #user2 sends message
    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user2['token'],
        'dm_id': dm_id1,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #user2 shares message to user3
    resp = requests.post(config.url + 'message/share/v1', json={
        'token': user2['token'],
        'og_message_id' : m_id1,
        'message': '',
        'channel_id': -1,
        'dm_id' : dm_id2,
    })
    assert resp.status_code == 403

def test_message_senddm():

    #TEST MESSAGE SEND DM

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id1 = resp.json()['dm_id']

    #user1 sends message
    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1['token'],
        'dm_id': dm_id1,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()
    assert m_id1 == 1

    #obtain message contents
    resp = requests.get(config.url + 'dm/messages/v1', json={
        'token': user1['token'],
        'dm_id': dm_id1,
        'start': 0,
    })
    message_list = resp.json()['messages'][0]['message']
    assert resp.status_code == 200
    assert message_list == "Hello World!"

    #TEST MESSAGE SEND DM INPUT ERROR FOR MESSAGE LENGTH > 1000

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id1 = resp.json()['dm_id']

    #user1 sends message of length 1001
    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1['token'],
        'dm_id': dm_id1,
        'message': 1001*'h',
    })
    assert resp.status_code == 400

    #TEST MESSAGE SEND DM ACCESS ERROR FOR USER NOT IN DM

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #register user3
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Chau@gmail.com',
        'password': 'farmfiesta',
        'name_first': 'Poppy',
        'name_last': 'Chau',
    })
    assert resp.status_code == 200
    user3 = resp.json()

    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id1 = resp.json()['dm_id']

    #user1 sends message of length 1001
    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user3['token'],
        'dm_id': dm_id1,
        'message': 'hehexd',
    })
    assert resp.status_code == 403

def test_http_message_sendlater():

    #Test message_sendlater

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    send_time = datetime.timestamp(datetime.now()) + 2

    #owner sends message
    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
        'time_sent': send_time,
    })
    assert resp.status_code == 200

    #obtain message contents
    resp = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = resp.json()
    assert resp.status_code == 200
    assert len(message_list['messages']) == 0

    sleep(3)
    #obtain message contents after sleep
    resp = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = resp.json()
    assert resp.status_code == 200
    assert len(message_list['messages']) == 1


    #test message_sendlater for input error

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #time in the past
    send_time = datetime.timestamp(datetime.now()) - 2
    #owner sends message
    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
        'time_sent': send_time,
    })
    assert resp.status_code == 400

    #invalid channel
    send_time = datetime.timestamp(datetime.now()) + 2
    #owner sends message
    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': owner['token'],
        'channel_id': 3,
        'message': 'Hello World!',
        'time_sent': send_time,
    })
    assert resp.status_code == 400

    #invalid message length
    send_time = datetime.timestamp(datetime.now()) + 2
    #owner sends message
    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 1001*'h',
        'time_sent': send_time,
    })
    assert resp.status_code == 400

    #Test message_sendlater for access error

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #register user
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'circus123',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user = resp.json()
    send_time = datetime.timestamp(datetime.now()) + 2

    #user sends message
    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
        'time_sent': send_time,
    })
    assert resp.status_code == 403

def test_http_message_sendlaterdm():

    #test message_sendlaterdm

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id1 = resp.json()['dm_id']
    send_time = datetime.timestamp(datetime.now()) + 2

    #user1 sends message
    resp = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user1['token'],
        'dm_id': dm_id1,
        'message': 'Hello World!',
        'time_sent': send_time
    })
    assert resp.status_code == 200


    #obtain message contents
    resp = requests.get(config.url + 'dm/messages/v1', json={
        'token': user1['token'],
        'dm_id': dm_id1,
        'start': 0,
    })
    message_list = resp.json()
    assert resp.status_code == 200
    assert len(message_list['messages']) == 0

    sleep(3)
    #obtain message contents after sleep
    resp = requests.get(config.url + 'dm/messages/v1', json={
        'token': user1['token'],
        'dm_id': dm_id1,
        'start': 0,
    })
    message_list = resp.json()
    assert resp.status_code == 200
    assert len(message_list['messages']) == 1

    #test message_sendlaterdm for input error

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id1 = resp.json()['dm_id']

    #time is in past
    send_time = datetime.timestamp(datetime.now()) - 2
    #user1 sends message
    resp = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user1['token'],
        'dm_id': dm_id1,
        'message': 'Hello World!',
        'time_sent': send_time
    })
    assert resp.status_code == 400

    #invalid channel
    send_time = datetime.timestamp(datetime.now()) + 2
    #user1 sends message
    resp = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user1['token'],
        'dm_id': 3,
        'message': 'Hello World!',
        'time_sent': send_time
    })
    assert resp.status_code == 400

    #invalid message length
    send_time = datetime.timestamp(datetime.now()) + 2
    #user1 sends message
    resp = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user1['token'],
        'dm_id': dm_id1,
        'message': 1001*'h',
        'time_sent': send_time
    })
    assert resp.status_code == 400

    #test message_sendlaterdm for access error

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #register user3
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'poppypro@gmail.com',
        'password': 'fiesta123',
        'name_first': 'Ethan',
        'name_last': 'Ethanson',
    })
    assert resp.status_code == 200
    user3 = resp.json()

    #create dm1
    resp = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']],
    })
    assert resp.status_code == 200
    dm_id1 = resp.json()['dm_id']

    send_time = datetime.timestamp(datetime.now()) + 2

    #user3 sends message
    resp = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user3['token'],
        'dm_id': dm_id1,
        'message': 'Hello World!',
        'time_sent': send_time
    })
    assert resp.status_code == 403

def test_http_message_react():

    #test message_react

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register new user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #invite user 1
    resp = requests.post(config.url + 'channel/join/v2', json={
        'token': user1['token'],
        'channel_id': channel_id,
    })
    assert resp.status_code == 200

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()

    #user reacts to message
    resp = requests.post(config.url + 'message/react/v1', json={
        'token': user1['token'],
        'message_id': m_id1,
        'react_id': 1,
    })
    assert resp.status_code == 200

    #obtain message contents
    resp = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = resp.json()['messages'][0]['reacts'][0]
    assert resp.status_code == 200
    assert message_list['react_id'] == 1
    assert message_list['u_ids'] == [user1['auth_user_id']]

    #test message_react for input error

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register new user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #invite user 1
    resp = requests.post(config.url + 'channel/join/v2', json={
        'token': user1['token'],
        'channel_id': channel_id,
    })
    assert resp.status_code == 200

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()

    #incorrect message id
    #user reacts to message
    resp = requests.post(config.url + 'message/react/v1', json={
        'token': user1['token'],
        'message_id': 3,
        'react_id': 1,
    })
    assert resp.status_code == 400

    #invalid react id
    resp = requests.post(config.url + 'message/react/v1', json={
        'token': user1['token'],
        'message_id': m_id1,
        'react_id': 3,
    })
    assert resp.status_code == 400

    #user had alreeady reacted
    #user reacts to message
    resp = requests.post(config.url + 'message/react/v1', json={
        'token': user1['token'],
        'message_id': m_id1,
        'react_id': 1,
    })
    assert resp.status_code == 200

    #user reacts to message again
    resp = requests.post(config.url + 'message/react/v1', json={
        'token': user1['token'],
        'message_id': m_id1,
        'react_id': 1,
    })
    assert resp.status_code == 400

    #test for message_react access error

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register new user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register new user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Poppy@gmail.com',
        'password': 'fiesta22',
        'name_first': 'Ethan',
        'name_last': 'Ethanson',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #invite user 1
    resp = requests.post(config.url + 'channel/join/v2', json={
        'token': user1['token'],
        'channel_id': channel_id,
    })
    assert resp.status_code == 200

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()

    #invalid user
    #user2 reacts to message
    resp = requests.post(config.url + 'message/react/v1', json={
        'token': user2['token'],
        'message_id': m_id1,
        'react_id': 1,
    })
    assert resp.status_code == 403

def test_http_message_unreact():
    #test message_unreact

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register new user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #invite user 1
    resp = requests.post(config.url + 'channel/join/v2', json={
        'token': user1['token'],
        'channel_id': channel_id,
    })
    assert resp.status_code == 200

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()

    #user reacts to message
    resp = requests.post(config.url + 'message/react/v1', json={
        'token': user1['token'],
        'message_id': m_id1,
        'react_id': 1,
    })
    assert resp.status_code == 200

    #user unreacts to message
    resp = requests.post(config.url + 'message/unreact/v1', json={
        'token': user1['token'],
        'message_id': m_id1,
        'react_id': 1,
    })
    assert resp.status_code == 200

    #obtain message contents
    resp = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = resp.json()['messages'][0]['reacts']
    assert resp.status_code == 200
    assert len(message_list) == 0

    #Test message_unreact for input error

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register new user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #invite user 1
    resp = requests.post(config.url + 'channel/join/v2', json={
        'token': user1['token'],
        'channel_id': channel_id,
    })
    assert resp.status_code == 200

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()

    #user reacts to message
    resp = requests.post(config.url + 'message/react/v1', json={
        'token': user1['token'],
        'message_id': m_id1,
        'react_id': 1,
    })
    assert resp.status_code == 200

    #invalid message id
    #user unreacts to message
    resp = requests.post(config.url + 'message/unreact/v1', json={
        'token': user1['token'],
        'message_id': 3,
        'react_id': 1,
    })
    assert resp.status_code == 400

    #invalid react id
    #user unreacts to message
    resp = requests.post(config.url + 'message/unreact/v1', json={
        'token': user1['token'],
        'message_id': m_id1,
        'react_id': 3,
    })
    assert resp.status_code == 400

    #user has already uncreated
    #user unreacts to message
    resp = requests.post(config.url + 'message/unreact/v1', json={
        'token': user1['token'],
        'message_id': m_id1,
        'react_id': 1,
    })
    assert resp.status_code == 200

    #user unreacts to message again
    resp = requests.post(config.url + 'message/unreact/v1', json={
        'token': user1['token'],
        'message_id': m_id1,
        'react_id': 1,
    })
    assert resp.status_code == 400

    #test message_unreact for access error

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Stevenson@gmail.com',
        'password': 'zap123',
        'name_first': 'Steven',
        'name_last': 'Stevenson',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register new user1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'monkeycircus',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    user1 = resp.json()

    #register new user2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Poppy@gmail.com',
        'password': 'fiesta22',
        'name_first': 'Ethan',
        'name_last': 'Ethanson',
    })
    assert resp.status_code == 200
    user2 = resp.json()

    #create channel
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id = resp.json()['channel_id']

    #invite user 1
    resp = requests.post(config.url + 'channel/join/v2', json={
        'token': user1['token'],
        'channel_id': channel_id,
    })
    assert resp.status_code == 200

    #owner sends message
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'message': 'Hello World!',
    })
    assert resp.status_code == 200
    m_id1 = resp.json()

    #user1 reacts to message
    resp = requests.post(config.url + 'message/react/v1', json={
        'token': user1['token'],
        'message_id': m_id1,
        'react_id': 1,
    })
    assert resp.status_code == 200

    #invalid user
    #user2 unreacts message
    resp = requests.post(config.url + 'message/unreact/v1', json={
        'token': user2['token'],
        'message_id': m_id1,
        'react_id': 1,
    })
    assert resp.status_code == 403

def test_http_message_pin():
    '''
    HTTP test for message_pin for where all parameters are valid
    '''
    # Resets the internal data of the application to it's initial state
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    # Register owner
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'john.smith@gmail.com',
        'password': 'pass123',
        'name_first': 'John',
        'name_last': 'Smith',
    })
    assert res.status_code == 200
    owner = res.json()

    # Register member
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'eliza.jones@gmail.com',
        'password': 'pass123',
        'name_first': 'Eliza',
        'name_last': 'Jones',
    })
    assert res.status_code == 200
    member = res.json()

    # Create Channel
    res = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Test Channel',
        'is_public': True,
    })
    assert res.status_code == 200
    channel = res.json()

    # User joins channel
    res = requests.post(config.url + 'channel/join/v2', json={
        'token': member['token'],
        'channel_id': channel['channel_id'],
    })
    assert res.status_code == 200

    # Send message to channel
    res = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200
    msg_id = res.json()

    # pin message
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': owner['token'],
        'message_id': msg_id,
    })
    assert res.status_code == 200

    # get message list
    res = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'start': 0,
    })
    assert res.status_code == 200
    message_list = res.json()
    assert message_list['messages'][0]['is_pinned'] == True

    # Create DM
    res = requests.post(config.url + 'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member['auth_user_id']],
    })
    assert res.status_code == 200
    dm = res.json()

    # Send message to dm
    res = requests.post(config.url + 'message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200
    msg_id = res.json()

    # pin message
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': owner['token'],
        'message_id': msg_id,
    })
    assert res.status_code == 200

    # get message list
    res = requests.get(config.url + 'dm/messages/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'start': 0,
    })
    assert res.status_code == 200
    message_list = res.json()
    assert message_list['messages'][0]['is_pinned'] == True

def test_http_message_pin_input_error():
    '''
    HTTP test for message_pin for input errors (invalid msg_id or msg already
                                                pinned)
    '''
    # Resets the internal data of the application to it's initial state
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    # Register owner
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'john.smith@gmail.com',
        'password': 'pass123',
        'name_first': 'John',
        'name_last': 'Smith',
    })
    assert res.status_code == 200
    owner = res.json()

    # Create Channel
    res = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Test Channel',
        'is_public': True,
    })
    assert res.status_code == 200
    channel = res.json()

    # Send message
    res = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200
    msg_id = res.json()

    # pin message
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': owner['token'],
        'message_id': msg_id,
    })
    assert res.status_code == 200

    # pin message with invalid msg_id
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': owner['token'],
        'message_id': msg_id+100,
    })
    assert res.status_code == 400

    # msg already pinned
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': owner['token'],
        'message_id': msg_id,
    })
    assert res.status_code == 400

def test_http_message_pin_access_error():
    '''
    HTTP test for message_pin for access errors (auth user not in channel or
                                                not owner)
    '''
    # Resets the internal data of the application to it's initial state
    assert requests.delete(config.url + 'clear/v1').status_code == 200
    # Register owner
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'john.smith@gmail.com',
        'password': 'pass123',
        'name_first': 'John',
        'name_last': 'Smith',
    })
    assert res.status_code == 200
    owner = res.json()

    # Register member
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'eliza.jones@gmail.com',
        'password': 'pass123',
        'name_first': 'Eliza',
        'name_last': 'Jones',
    })
    assert res.status_code == 200
    member = res.json()

    # Register member
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'ethan.ethanson@gmail.com',
        'password': 'pass123',
        'name_first': 'Ethan',
        'name_last': 'Ethanson',
    })
    assert res.status_code == 200
    member2 = res.json()

    # Create Channel
    res = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Test Channel',
        'is_public': True,
    })
    assert res.status_code == 200
    channel = res.json()

    # Send message to channel
    res = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200
    msg_id1 = res.json()

    # Create DM
    res = requests.post(config.url + 'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member['auth_user_id']],
    })
    assert res.status_code == 200
    dm = res.json()

    # Send message to dm
    res = requests.post(config.url + 'message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200
    msg_id2 = res.json()

    # not in channel
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': member['token'],
        'message_id': msg_id1,
    })
    assert res.status_code == 403

    # not in dm
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': member2['token'],
        'message_id': msg_id2,
    })
    assert res.status_code == 403

    # User joins channel
    res = requests.post(config.url + 'channel/join/v2', json={
        'token': member['token'],
        'channel_id': channel['channel_id'],
    })

    # user not owner in channel
    assert res.status_code == 200
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': member['token'],
        'message_id': msg_id1,
    })
    assert res.status_code == 403

    # user not owner in dm
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': member['token'],
        'message_id': msg_id2,
    })
    assert res.status_code == 403

def test_http_message_unpin():
    '''
    HTTP test for message_unpin for where all parameters are valid
    '''
    # Resets the internal data of the application to it's initial state
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    # Register owner
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'john.smith@gmail.com',
        'password': 'pass123',
        'name_first': 'John',
        'name_last': 'Smith',
    })
    assert res.status_code == 200
    owner = res.json()

    # Register member
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'eliza.jones@gmail.com',
        'password': 'pass123',
        'name_first': 'Eliza',
        'name_last': 'Jones',
    })
    assert res.status_code == 200
    member = res.json()

    # Create Channel
    res = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Test Channel',
        'is_public': True,
    })
    assert res.status_code == 200
    channel = res.json()

    # User joins channel
    res = requests.post(config.url + 'channel/join/v2', json={
        'token': member['token'],
        'channel_id': channel['channel_id'],
    })
    assert res.status_code == 200

    # Send message to channel
    res = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200
    msg_id = res.json()

    # pin message
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': owner['token'],
        'message_id': msg_id,
    })
    assert res.status_code == 200

    # unpin message
    res = requests.post(config.url + 'message/unpin/v1', json={
        'token': owner['token'],
        'message_id': msg_id,
    })
    assert res.status_code == 200

    # get message list
    res = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'start': 0,
    })
    assert res.status_code == 200
    message_list = res.json()
    assert message_list['messages'][0]['is_pinned'] == False

    # Create DM
    res = requests.post(config.url + 'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member['auth_user_id']],
    })
    assert res.status_code == 200
    dm = res.json()

    # Send message to dm
    res = requests.post(config.url + 'message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200
    msg_id = res.json()

    # pin message
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': owner['token'],
        'message_id': msg_id,
    })
    assert res.status_code == 200

    # unpin message
    res = requests.post(config.url + 'message/unpin/v1', json={
        'token': owner['token'],
        'message_id': msg_id,
    })
    assert res.status_code == 200

    # get message list
    res = requests.get(config.url + 'dm/messages/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'start': 0,
    })
    assert res.status_code == 200
    message_list = res.json()
    assert message_list['messages'][0]['is_pinned'] == False

def test_http_message_unpin_input_error():
    '''
    HTTP test for message_unpin for input errors (invalid msg_id or msg already
                                                pinned)
    '''
    # Resets the internal data of the application to it's initial state
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    # Register owner
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'john.smith@gmail.com',
        'password': 'pass123',
        'name_first': 'John',
        'name_last': 'Smith',
    })
    assert res.status_code == 200
    owner = res.json()

    # Create Channel
    res = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Test Channel',
        'is_public': True,
    })
    assert res.status_code == 200
    channel = res.json()

    # Send message
    res = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200
    msg_id = res.json()

    # pin message with invalid msg_id
    res = requests.post(config.url + 'message/unpin/v1', json={
        'token': owner['token'],
        'message_id': msg_id+100,
    })
    assert res.status_code == 400

    # msg already unpinned
    res = requests.post(config.url + 'message/unpin/v1', json={
        'token': owner['token'],
        'message_id': msg_id,
    })
    assert res.status_code == 400

def test_http_message_unpin_access_error():
    '''
    HTTP test for message_unpin for access errors (auth user not in channel or
                                                not owner)
    '''
    # Resets the internal data of the application to it's initial state
    assert requests.delete(config.url + 'clear/v1').status_code == 200
    # Register owner
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'john.smith@gmail.com',
        'password': 'pass123',
        'name_first': 'John',
        'name_last': 'Smith',
    })
    assert res.status_code == 200
    owner = res.json()

    # Register member
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'eliza.jones@gmail.com',
        'password': 'pass123',
        'name_first': 'Eliza',
        'name_last': 'Jones',
    })
    assert res.status_code == 200
    member = res.json()

    # Register member
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'ethan.ethanson@gmail.com',
        'password': 'pass123',
        'name_first': 'Ethan',
        'name_last': 'Ethanson',
    })
    assert res.status_code == 200
    member2 = res.json()

    # Create Channel
    res = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': 'Test Channel',
        'is_public': True,
    })
    assert res.status_code == 200
    channel = res.json()

    # Send message to channel
    res = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200
    msg_id1 = res.json()

    # Create DM
    res = requests.post(config.url + 'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member['auth_user_id']],
    })
    assert res.status_code == 200
    dm = res.json()

    # Send message to dm
    res = requests.post(config.url + 'message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200
    msg_id2 = res.json()

    # pin msg to dm and channel
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': owner['token'],
        'message_id': msg_id1,
    })
    assert res.status_code == 200
    res = requests.post(config.url + 'message/pin/v1', json={
        'token': owner['token'],
        'message_id': msg_id2,
    })
    assert res.status_code == 200

    # not in channel
    res = requests.post(config.url + 'message/unpin/v1', json={
        'token': member['token'],
        'message_id': msg_id1,
    })
    assert res.status_code == 403

    # not in dm
    res = requests.post(config.url + 'message/unpin/v1', json={
        'token': member2['token'],
        'message_id': msg_id2,
    })
    assert res.status_code == 403

    # User joins channel
    res = requests.post(config.url + 'channel/join/v2', json={
        'token': member['token'],
        'channel_id': channel['channel_id'],
    })

    # user not owner in channel
    assert res.status_code == 200
    res = requests.post(config.url + 'message/unpin/v1', json={
        'token': member['token'],
        'message_id': msg_id1,
    })
    assert res.status_code == 403

    # user not owner in dm
    res = requests.post(config.url + 'message/unpin/v1', json={
        'token': member['token'],
        'message_id': msg_id2,
    })
    assert res.status_code == 403
