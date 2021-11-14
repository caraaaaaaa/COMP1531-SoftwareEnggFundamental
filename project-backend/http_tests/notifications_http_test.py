import pytest
import requests
import json
from src import config
from time import sleep
def test_notifications_get_dm():
    #test notifications are raised when invited and tagged in dms
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
    
    #find user handle for owner1
    resp = requests.get(config.url+'user/profile/v2', json={
        'token': owner1['token'],
        'u_id': owner1['auth_user_id']
    })
    assert resp.status_code == 200
    owner_handle = resp.json()['handle_str']

    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'two@gmail.com',
        'password': 'pass123',
        'name_first': 'two',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    member1 = resp.json()
    
    #find user handle for member1
    resp = requests.get(config.url+'user/profile/v2', json={
        'token': member1['token'],
        'u_id': member1['auth_user_id']
    })
    assert resp.status_code == 200
    member_handle = resp.json()['handle_str']

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
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [member1['auth_user_id']],
    })
    assert resp.status_code == 200
    dm = resp.json()
    
    #get notifications for member1
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': member1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    assert len(notif['notifications']) == 1
    assert notif['notifications'] == [{
        'channel_id': -1,
        'dm_id': dm['dm_id'],
        'notification_message': f"{owner_handle} added you to {dm['dm_name']}"  
    }]
    
    #invite member2 into dm1
    resp = requests.post(config.url+'dm/invite/v1', json={
        'token': owner1['token'],
        'dm_id': dm['dm_id'],        
        'u_id': member2['auth_user_id'],
    })
    assert resp.status_code == 200
    
    #get notifications for member2
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': member2['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    assert len(notif['notifications']) == 1
    assert notif['notifications'] == [{
        'channel_id': -1,
        'dm_id': dm['dm_id'],
        'notification_message': f"{owner_handle} added you to {dm['dm_name']}"  
    }]
    
    #member1 gets tagged in dm message by owner1
    
    message = f"hey, @{member_handle}"
    resp = requests.post(config.url+'message/senddm/v1', json={
        'token': owner1['token'],
        'dm_id': dm['dm_id'],
        'message': message,
    })
    assert resp.status_code == 200
    
    #get notifications for member1
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': member1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    assert len(notif['notifications']) == 2
    assert notif['notifications'][0] == { 
        'channel_id': -1,
        'dm_id': dm['dm_id'],
        'notification_message': f"{owner_handle} tagged you in {dm['dm_name']}: {message[0:20]}"  
    }
    
    
def test_notifications_get_channels():
    #test notifications are raised when invited and tagged in channels
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
    
    #find user handle for owner1
    resp = requests.get(config.url+'user/profile/v2', json={
        'token': owner1['token'],
        'u_id': owner1['auth_user_id'],
    })
    assert resp.status_code == 200
    owner_handle = resp.json()['handle_str']

    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'two@gmail.com',
        'password': 'pass123',
        'name_first': 'two',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    member1 = resp.json()
    
    #find user handle for member1
    resp = requests.get(config.url+'user/profile/v2', json={
        'token': member1['token'],
        'u_id': member1['auth_user_id'],
    })
    assert resp.status_code == 200
    member_handle = resp.json()['handle_str']

    #create channel1
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'myChannel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel1 = resp.json()
    
    #invite member1 to channel
    resp = requests.post(config.url+'channel/invite/v2', json={
        'token': owner1['token'],
        'channel_id': channel1['channel_id'],
        'u_id': member1['auth_user_id'],
    })
    assert resp.status_code == 200
    
    #get channel1 details
    resp = requests.get(config.url+'channel/details/v2', json={
        'token': member1['token'],
        'channel_id': channel1['channel_id'],
    })
    assert resp.status_code == 200
    details = resp.json()
    
    #get notifications for member1
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': member1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    assert len(notif['notifications']) == 1
    assert notif['notifications'] == [{
        'channel_id': channel1['channel_id'],
        'dm_id': -1,
        'notification_message': f"{owner_handle} added you to {details['name']}"  
    }]
       
    #member1 gets tagged in dm message by owner1
    
    message = f"hey, @{member_handle}"
    resp = requests.post(config.url+'message/send/v2', json={
        'token': owner1['token'],
        'channel_id': channel1['channel_id'],
        'message': message,
    })
    assert resp.status_code == 200
    
    #get notifications for member1
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': member1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    assert len(notif['notifications']) == 2
    assert notif['notifications'][0] == { 
        'channel_id': channel1['channel_id'],
        'dm_id': -1,
        'notification_message': f"{owner_handle} tagged you in {details['name']}: {message[0:20]}"  
    }
    
def test_more_messages():
    #test the 20 most recent notifications are displayed
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
    
    #find user handle for owner1
    resp = requests.get(config.url+'user/profile/v2', json={
        'token': owner1['token'],
        'u_id': owner1['auth_user_id'],
    })
    assert resp.status_code == 200
    owner_handle = resp.json()['handle_str']
    
    #create dm1
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': []
    })
    assert resp.status_code == 200
    dm = resp.json()
    
    message = f"Just talking to myself @{owner_handle}"
    #send 20 messages, each of which the owner tags himself in
    counter = 0
    while counter < 20:
        resp = requests.post(config.url+'message/senddm/v1', json={
            'token': owner1['token'],
            'dm_id': dm['dm_id'],
            'message': message,
        })
        assert resp.status_code == 200
        counter += 1
    
    #get notifications for owner1
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    
    assert len(notif['notifications']) == 20
    assert notif['notifications'][19]['notification_message'] == f"{owner_handle} tagged you in {dm['dm_name']}: {message[0:20]}"
    
    #send one more message to check if the last 20 messages are sent 
    # (total 21 messages sent after sending one more)
    resp = requests.post(config.url+'message/senddm/v1', json={
        'token': owner1['token'],
        'dm_id': dm['dm_id'],
        'message': message,
    })
    assert resp.status_code == 200
    
    #get notifications for owner1
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    
    assert len(notif['notifications']) == 20

def test_message_share():
    #Test if the notifications is raised when a message with a tag is shared
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
    
    #find user handle for owner1
    resp = requests.get(config.url+'user/profile/v2', json={
        'token': owner1['token'],
        'u_id': owner1['auth_user_id'],
    })
    assert resp.status_code == 200
    owner_handle = resp.json()['handle_str']
    
    #create dm1
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': []
    })
    assert resp.status_code == 200
    dm1 = resp.json()
    
    #create dm1
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': []
    })
    assert resp.status_code == 200
    dm2 = resp.json()
    
    message = f"Just talking to myself @{owner_handle}"
    
    #send message to dm1, tagging owner1
    resp = requests.post(config.url+'message/senddm/v1', json={
            'token': owner1['token'],
            'dm_id': dm1['dm_id'],
            'message': message,
    })
    assert resp.status_code == 200
    message = resp.json()
    
    #share this message to dm2
    resp = requests.post(config.url+'message/share/v1', json={
        'token': owner1['token'],
        'og_message_id': message,
        'message': '',
        'channel_id': -1,
        'dm_id': dm2['dm_id'],
    })
    assert resp.status_code == 200
    
    #get notifications for owner1
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    
    assert len(notif['notifications']) == 2


def test_invalid_token():
    #Test for invalid token
    #clear
    assert requests.delete(config.url+'clear/v1').status_code == 200
    
    #view notifications with invalid token
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': 0,
    })
    assert resp.status_code == 403
        
    #view notifications with invalid token
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': {},
    })
    assert resp.status_code == 403
    
    #view notifications with invalid token
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': '1234',
    })
    assert resp.status_code == 403
    
def test_no_notifications():
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
    
    #view notifications with invalid token
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    
    assert notif['notifications'] == []

def test_multiple_tags():
    #test notifications are raised for the respective number of unique tags in a message
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
    
    #find user handle for owner1
    resp = requests.get(config.url+'user/profile/v2', json={
        'token': owner1['token'],
        'u_id': owner1['auth_user_id'],
    })
    assert resp.status_code == 200
    owner_handle = resp.json()['handle_str']

    #register member1
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'two@gmail.com',
        'password': 'pass123',
        'name_first': 'two',
        'name_last': 'last',
    })
    assert resp.status_code == 200
    member1 = resp.json()
    
    #find user handle for member1
    resp = requests.get(config.url+'user/profile/v2', json={
        'token': member1['token'],
        'u_id': owner1['auth_user_id'],
    })
    
    assert resp.status_code == 200
    member_handle = resp.json()['handle_str']

    #create dm1
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [member1['auth_user_id']],
    })
    assert resp.status_code == 200
    dm = resp.json()

    #member1 gets tagged in dm message by owner1
    message = f"hey, @{member_handle} and myself @{owner_handle}"
    resp = requests.post(config.url+'message/senddm/v1', json={
        'token': owner1['token'],
        'dm_id': dm['dm_id'],
        'message': message,
    })
    assert resp.status_code == 200
    
    #get notifications for member1
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': member1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    assert len(notif['notifications']) == 2
    
    #get notifications for owner1
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    assert len(notif['notifications']) == 1
    assert notif['notifications'][0] == { 
        'channel_id': -1,
        'dm_id': dm['dm_id'],
        'notification_message': f"{owner_handle} tagged you in {dm['dm_name']}: {message[0:20]}"  
    }

def test_notifications_message_react():
    '''Test notifications are raised when any person reacts to a user's message'''
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
    
    #find user handle for owner1
    resp = requests.get(config.url+'user/profile/v2', json={
        'token': owner1['token'],
        'u_id': owner1['auth_user_id'],
    })
    assert resp.status_code == 200
    owner_handle = resp.json()['handle_str']
    
    #create a channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()
    
    #create dm
    resp = requests.post(config.url+'dm/create/v1', json={
        'token': owner1['token'],
        'u_ids': [],
    })
    assert resp.status_code == 200
    dm = resp.json()
    
    
    #send message to dm
    resp = requests.post(config.url+'message/senddm/v1', json={
        'token': owner1['token'],
        'dm_id': dm['dm_id'],
        'message': 'hello',
    })
    assert resp.status_code == 200
    message = resp.json()
    
    #react to message in dm
    resp = requests.post(config.url+'message/react/v1', json={
        'token': owner1['token'],
        'message_id': message,
        'react_id': 1,
    })
        
    #send message to channel
    resp = requests.post(config.url+'message/send/v2', json={
        'token': owner1['token'],
        'channel_id': channel['channel_id'],
        'message': 'bruh',
    })
    assert resp.status_code == 200
    message = resp.json()
    
    #react to message in channel
    resp = requests.post(config.url+'message/react/v1', json={
        'token': owner1['token'],
        'message_id': message,
        'react_id': 1,
    })
    
    #get channel details
    resp = requests.get(config.url+'channel/details/v2', json={
        'token': owner1['token'],
        'channel_id': channel['channel_id'],
    })
    assert resp.status_code == 200
    details = resp.json()
    
    #get notifications
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    
    assert len(notif['notifications']) == 2
    assert notif['notifications'] == [{
        'channel_id': channel['channel_id'],
        'dm_id': -1,
        'notification_message': f"{owner_handle} reacted to your message in {details['name']}",
    },
    {
        'channel_id': -1,
        'dm_id': dm['dm_id'],
        'notification_message': f"{owner_handle} reacted to your message in {dm['dm_name']}",
    }]

def test_notifications_standup():
    '''Test notifications are raised when standup message is sent with a tag'''
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
    
    #find user handle for owner1
    resp = requests.get(config.url+'user/profile/v2', json={
        'token': owner1['token'],
        'u_id': owner1['auth_user_id'],
    })
    assert resp.status_code == 200
    owner_handle = resp.json()['handle_str']
    
    #create a channel
    resp = requests.post(config.url+'channels/create/v2', json={
        'token': owner1['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    assert resp.status_code == 200
    channel = resp.json()
    
    #start standup
    resp = requests.post(config.url+'standup/start/v1', json={
        'token': owner1['token'],
        'channel_id': channel['channel_id'],
        'length': 5,
    })
    assert resp.status_code == 200
    
    #owner1 send message to standup
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': owner1['token'],
        'channel_id': channel['channel_id'],
        'message': f'@{owner_handle} hello',
    })
    assert resp.status_code == 200
    
    #owner1 send another message to standup
    resp = requests.post(config.url+'standup/send/v1', json={
        'token': owner1['token'],
        'channel_id': channel['channel_id'],
        'message': f'how are you?',
    })
    assert resp.status_code == 200
    
    #request channel details
    resp = requests.get(config.url+'channel/details/v2', json={
        'token': owner1['token'],
        'channel_id': channel['channel_id'],
    })
    assert resp.status_code == 200
    details = resp.json()
    
    sleep(5)
    
    #check channel messages
    resp = requests.get(config.url+'channel/messages/v2', json={
        'token': owner1['token'],
        'channel_id': channel['channel_id'],
        'start': 0,
    })
    assert resp.status_code == 200
    message = resp.json()
    assert len(message['messages']) == 1
    
    #get notifications for owner1
    resp = requests.get(config.url+'notifications/get/v1', json={
        'token': owner1['token'],
    })
    assert resp.status_code == 200
    notif = resp.json()
    
    assert len(notif['notifications']) == 1
    assert notif['notifications'][0] == { 
        'channel_id': channel['channel_id'],
        'dm_id': -1,
        'notification_message': f"{owner_handle} tagged you in {details['name']}: {message['messages'][0]['message'][0:20]}"  
    }
    
    
    
    
        
    
    

