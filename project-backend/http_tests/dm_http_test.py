import pytest
import json
import requests
from src import config
from src.dm import messageList

def test_dm_invite():
    #test basic functionality of dm/invite/v1 route

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'benji@gmail.com',
        'password': 'pass123',
        'name_first': 'Benji',
        'name_last': 'Choi',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'matthew@gmail.com',
        'password': 'pass123',
        'name_first': 'Matthew',
        'name_last': 'Choi',
    })
    assert resp.status_code == 200
    member1 = resp.json()

    #register member2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'kevin@gmail.com',
        'password': 'pass123',
        'name_first': 'Kevin',
        'name_last': 'Zhou',
    })
    assert resp.status_code == 200
    member2 = resp.json()

    #create dm
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']],
    })
    assert resp.status_code == 200
    dm = resp.json()

    #invite member2 to dm
    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'u_id': member2['auth_user_id'],
    })
    assert resp.status_code == 200
    dm_invite = resp.json()

    assert dm_invite == {}

    #dm details
    resp = requests.get(config.url+'dm/details/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 200
    dm_details = resp.json()

    assert len(dm_details['members']) == 3

    #invalid token

    #register non-member 1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'one@gmail.com',
        'password': 'pass123',
        'name_first': 'One',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    nonmember1 = resp.json()


    #register non-member 2
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'two@gmail.com',
        'password': 'pass123',
        'name_first': 'Two',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    nonmember2 = resp.json()


    #register non-member 3
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'three@gmail.com',
        'password': 'pass123',
        'name_first': 'Benji',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    nonmember3 = resp.json()

    #dm invite invalid tokens
    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': 0,
        'dm_id': dm['dm_id'],
        'u_id': nonmember1['auth_user_id'],
    })
    assert resp.status_code == 403

    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': {},
        'dm_id': dm['dm_id'],
        'u_id': nonmember1['auth_user_id'],
    })
    assert resp.status_code == 403

    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': nonmember1['token'],
        'dm_id': dm['dm_id'],
        'u_id': nonmember2['auth_user_id'],
    })
    assert resp.status_code == 403

    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': nonmember2['token'],
        'dm_id': dm['dm_id'],
        'u_id': nonmember1['auth_user_id'],
    })
    assert resp.status_code == 403

    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': nonmember3['token'],
        'dm_id': dm['dm_id'],
        'u_id': nonmember1['auth_user_id'],
    })
    assert resp.status_code == 403

    #test /dm/invite/v1 invalid user
    #clear
    assert requests.delete(config.url+'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'benji@gmail.com',
        'password': 'pass123',
        'name_first': 'Benji',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'matthew@gmail.com',
        'password': 'pass123',
        'name_first': 'Matthew',
        'name_last': 'Choi',
    })
    assert resp.status_code == 200
    member1 = resp.json()

    #create dm
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']],
    })
    assert resp.status_code == 200
    dm = resp.json()

    #invite invalid user to dm
    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'u_id': 0,
    })
    assert resp.status_code == 400

    #invite invalid user to dm
    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'u_id': {},
    })
    assert resp.status_code == 400

    #invite user that is already in dm
    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'u_id': owner['auth_user_id'],
    })
    assert resp.status_code == 400

    #test /dm/invite/v1 invalid dm_id

    #clear
    assert requests.delete(config.url+'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'benji@gmail.com',
        'password': 'pass123',
        'name_first': 'Benji',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'matthew@gmail.com',
        'password': 'pass123',
        'name_first': 'Matthew',
        'name_last': 'Choi',
    })
    assert resp.status_code == 200
    member1 = resp.json()

    #invite to invalid dm
    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': owner['token'],
        'dm_id': 0,
        'u_id': member1['auth_user_id'],
    })
    assert resp.status_code == 400

    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': owner['token'],
        'dm_id': {},
        'u_id': member1['auth_user_id'],
    })
    assert resp.status_code == 400

def test_dm_leave_v1():
    #test basic functionality of /dm/leave/v1 route
    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'benji@gmail.com',
        'password': 'pass123',
        'name_first': 'Benji',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'matthew@gmail.com',
        'password': 'pass123',
        'name_first': 'Matthew',
        'name_last': 'Choi',
    })
    assert resp.status_code == 200
    member1 = resp.json()

    #create dm
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']],
    })
    assert resp.status_code == 200
    dm = resp.json()

    #leave dm
    resp = requests.post(config.url+'dm/leave/v1', json={
        'token': member1['token'],
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 200
    dm_leave = resp.json()

    assert dm_leave == {}

    #dm details
    resp = requests.get(config.url+'dm/details/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 200
    dm_details = resp.json()

    assert len(dm_details['members']) == 1

    #Test for invalid token
    #leave dm
    resp = requests.post(config.url+'dm/leave/v1', json={
        'token': {},
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 403

    #leave dm
    resp = requests.post(config.url+'dm/leave/v1', json={
        'token': 0,
        'dm_id': dm['dm_id'],
    })
    assert resp.status_code == 403

    #member1 leaving dm they already left
    #leave dm
    resp = requests.post(config.url+'dm/leave/v1', json={
        'token': member1['token'],
        'dm_id': dm['dm_id'],
    })

    assert resp.status_code == 403

    #Test for invalid dm_id
    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'benji@gmail.com',
        'password': 'pass123',
        'name_first': 'Benji',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'matthew@gmail.com',
        'password': 'pass123',
        'name_first': 'Matthew',
        'name_last': 'Choi',
    })
    assert resp.status_code == 200
    member1 = resp.json()

    #invite to invalid dm
    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': owner['token'],
        'dm_id': 0,
        'u_id': member1['auth_user_id'],
    })
    assert resp.status_code == 400

    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': owner['token'],
        'dm_id': {},
        'u_id': member1['auth_user_id'],
    })
    assert resp.status_code == 400
    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'benji@gmail.com',
        'password': 'pass123',
        'name_first': 'Benji',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'matthew@gmail.com',
        'password': 'pass123',
        'name_first': 'Matthew',
        'name_last': 'Choi',
    })
    assert resp.status_code == 200
    member1 = resp.json()

    #invite to invalid dm
    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': owner['token'],
        'dm_id': 0,
        'u_id': member1['auth_user_id'],
    })
    assert resp.status_code == 400

    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': owner['token'],
        'dm_id': {},
        'u_id': member1['auth_user_id'],
    })
    assert resp.status_code == 400

def test_dm_messages_v1():
    #test basic functionality of /dm/messages/v1 route
    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'benji@gmail.com',
        'password': 'pass123',
        'name_first': 'Benji',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'matthew@gmail.com',
        'password': 'pass123',
        'name_first': 'Matthew',
        'name_last': 'Choi',
    })
    assert resp.status_code == 200
    member1 = resp.json()

    #create dm
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']],
    })
    assert resp.status_code == 200
    dm = resp.json()

    msgString = 'How are you?'
    #send message to dm
    resp = requests.post(config.url+'message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': msgString
    })
    assert resp.status_code == 200
    dm_send = resp.json()

    #view messages in dm
    resp = requests.get(config.url+'dm/messages/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'start': 0
    })
    assert resp.status_code == 200
    dm_messages = resp.json()

    assert len(dm_messages['messages']) == 1
    print(dm_messages)
    assert dm_messages['messages'][0]['message_id'] == dm_send

    assert dm_messages['start'] == 0
    assert dm_messages['end'] == -1

    #send another message to verify whether the most recent messages are displayed first

    resp = requests.post(config.url+'message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': 'hey'
    })
    assert resp.status_code == 200
    dm_send = resp.json()

    #view messages in dm
    resp = requests.get(config.url+'dm/messages/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'start': 0
    })
    assert resp.status_code == 200
    dm_messages = resp.json()

    assert len(dm_messages['messages']) == 2

    assert dm_messages['messages'][0]['message_id'] == dm_send
    assert dm_messages['start'] == 0
    assert dm_messages['end'] == -1

    #test when 50 messages are sent

    messages = messageList(48)
    for message in messages:
        resp = requests.post(config.url+'message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': message,
        })
        assert resp.status_code == 200

    #view messages in dm
    resp = requests.get(config.url+'dm/messages/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'start': 0
    })
    assert resp.status_code == 200
    dm_messages = resp.json()
    assert len(dm_messages['messages']) == 50
    assert dm_messages['start'] == 0
    assert dm_messages['end'] == -1

    #Test when more than 50 messages are sent
    resp = requests.post(config.url+'message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': 'hey'
    })
    assert resp.status_code == 200

    #view messages in dm
    resp = requests.get(config.url+'dm/messages/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'start': 0
    })

    assert resp.status_code == 200
    dm_messages = resp.json()
    assert len(dm_messages['messages']) == 50
    assert dm_messages['start'] == 0
    assert dm_messages['end'] == 50

    #test for invalid token and dm

    #clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    #register owner
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'benji@gmail.com',
        'password': 'pass123',
        'name_first': 'Benji',
        'name_last': 'Marshall',
    })
    assert resp.status_code == 200
    owner = resp.json()

    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'matthew@gmail.com',
        'password': 'pass123',
        'name_first': 'Matthew',
        'name_last': 'Choi',
    })
    assert resp.status_code == 200
    member1 = resp.json()

    #register nonmember1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'jacob@gmail.com',
        'password': 'pass123',
        'name_first': 'Jacob',
        'name_last': 'Choi',
    })
    assert resp.status_code == 200
    nonmember1 = resp.json()

    #create dm
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']],
    })
    assert resp.status_code == 200

    #send message to dm
    resp = requests.post(config.url+'message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': 'hey'
    })
    assert resp.status_code == 200
    dm_send = resp.json()

    resp = requests.get(config.url+'dm/messages/v1', json={
        'token': 0,
        'dm_id': dm['dm_id'],
        'start': 0
    })
    assert resp.status_code == 403

    resp = requests.get(config.url+'dm/messages/v1', json={
        'token': {},
        'dm_id': dm['dm_id'],
        'start': 0
    })
    
    assert resp.status_code == 403
    
    resp = requests.get(config.url+'dm/messages/v1', json={
        'token': nonmember1['token'],
        'dm_id': dm['dm_id'],
        'start': 0
    })
    assert resp.status_code == 403

    #view messages using invalid dm

    resp = requests.get(config.url+'dm/messages/v1', json={
        'token': owner['token'],
        'dm_id': 0,
        'start': 0
    })
    assert resp.status_code == 400

    resp = requests.get(config.url+'dm/messages/v1', json={
        'token': owner['token'],
        'dm_id': {},
        'start': 0
    })
    assert resp.status_code == 400

    #test when start is greater than total messages

    resp  = requests.get(config.url+'dm/messages/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'start': 1
    })
    assert resp.status_code == 200

    #create dm
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': nonmember1['token'],
        'u_ids': [member1['auth_user_id']],
    })
    assert resp.status_code == 200
    dm = resp.json()

    #test when there are no messages to view

    resp = requests.get(config.url+'dm/messages/v1', json={
        'token': nonmember1['token'],
        'dm_id': dm['dm_id'],
        'start': 0
    })
    assert resp.status_code == 200

