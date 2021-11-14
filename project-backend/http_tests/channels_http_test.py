import pytest
import requests
import json
from src import config

def test_channels_create():

    #TEST FOR BASIC FUNCTIONALITY

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

    #create channel1
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200

    #get channels
    resp = requests.get(config.url + 'channels/listall/v2', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    channel_list2 = resp.json()
    assert channel_list2['channels'] == [
        {
            'channel_id' : 1,
            'name' : 'Channel_One'
        }
    ]

    #TEST CREATING MULTIPLE CHANNELS

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

    #create channel1
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200

    #create channel2
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel_Two',
        'is_public': True,
    })
    assert resp.status_code == 200

    #get channels
    resp = requests.get(config.url + 'channels/listall/v2', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    channel_list2 = resp.json()
    assert channel_list2['channels'] == [
        {
            'channel_id' : 1,
            'name' : 'Channel_One'
        },
        {
            'channel_id' : 2,
            'name' : 'Channel_Two'
        }
    ]

    #TEST FOR INVALID USER ID

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #create channel1
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': 2,
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 403

    #create channel2
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': 'wrong',
        'name': 'Channel_Two',
        'is_public': True,
    })
    assert resp.status_code == 403

    #create channel3
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': {},
        'name': 'Channel_Two',
        'is_public': True,
    })
    assert resp.status_code == 403

    #TEST FOR INVALID IS_PUBLIC PARAMETER

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

    #create channel1
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel_One',
        'is_public': 'True',
    })
    assert resp.status_code == 400

    #create channel2
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel_Two',
        'is_public': 3,
    })
    assert resp.status_code == 400

    #create channel3
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel_Two',
        'is_public': {},
    })
    assert resp.status_code == 400


def test_channels_list():

    #TEST FOR BASIC FUNCTIONALITY

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

    #create channel1
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id1 = resp.json()['channel_id']

    #create channel2
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel_Two',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id2 = resp.json()['channel_id']

    #register owner2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'clown123',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    owner2 = resp.json()

    #create channel3
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner2['token'],
        'name': 'Channel_Three',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id3 = resp.json()['channel_id']

    #call channels_list for owner1
    resp = requests.get(config.url + 'channels/list/v2', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    channel_list1 = resp.json()
    assert channel_list1['channels']  == [
        {
            'channel_id' : channel_id1,
            'name' : 'Channel_One'
        },
        {
            'channel_id' : channel_id2,
            'name' : 'Channel_Two'
        }
    ]
    #call channel_listall for owner1
    resp = requests.get(config.url + 'channels/listall/v2', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    channel_list2 = resp.json()
    assert channel_list2['channels']  == [
        {
            'channel_id' : channel_id1,
            'name' : 'Channel_One'
        },
        {
            'channel_id' : channel_id2,
            'name' : 'Channel_Two'
        },
        {
            'channel_id' : channel_id3,
            'name' : 'Channel_Three'
        }
    ]

    #TEST FOR PRIVATE LISTS

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

    #create channel1
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel_One',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel_id1 = resp.json()['channel_id']

    #create channel2
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel_Two',
        'is_public': False,
    })
    assert resp.status_code == 200
    channel_id2 = resp.json()['channel_id']

    #register owner2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'Johnson@gmail.com',
        'password': 'clown123',
        'name_first': 'John',
        'name_last': 'Johnson',
    })
    assert resp.status_code == 200
    owner2 = resp.json()

    #create channel3
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': owner2['token'],
        'name': 'Channel_Three',
        'is_public': False,
    })
    assert resp.status_code == 200
    channel_id3 = resp.json()['channel_id']

    #call channels_list for owner1
    resp = requests.get(config.url + 'channels/list/v2', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    channel_list1 = resp.json()
    assert channel_list1['channels']  == [
        {
            'channel_id' : channel_id1,
            'name' : 'Channel_One'
        },
        {
            'channel_id' : channel_id2,
            'name' : 'Channel_Two'
        }
    ]
    #call channel_listall for owner1
    resp = requests.get(config.url + 'channels/listall/v2', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    channel_list2 = resp.json()
    assert channel_list2['channels']  == [
        {
            'channel_id' : channel_id1,
            'name' : 'Channel_One'
        },
        {
            'channel_id' : channel_id2,
            'name' : 'Channel_Two'
        },
        {
            'channel_id' : channel_id3,
            'name' : 'Channel_Three'
        }
    ]

    #TEST FOR EMPTY LISTS

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

    #call channels_list for owner1
    resp = requests.get(config.url + 'channels/list/v2', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    channel_list1 = resp.json()
    assert channel_list1['channels']  == []

    #call channel_listall for owner1
    resp = requests.get(config.url + 'channels/listall/v2', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    channel_list2 = resp.json()
    assert channel_list2['channels']  == []

    #TEST FOR INVALID USER ID

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

    #call channels_list for no owner
    resp = requests.get(config.url + 'channels/list/v2', json={
        'token': [],
    })
    assert resp.status_code == 403

    #call channel_listall for owner1
    resp = requests.get(config.url + 'channels/listall/v2', json={
        'token': [],
    })
    assert resp.status_code == 403
