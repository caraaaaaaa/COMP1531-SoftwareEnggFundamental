import pytest
import urllib
import requests
import json
from src import config

# channel_details
def test_http_channel_details():
    '''
    HTTP test for channel_details for where all parameters are valid
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
        'name': 'Channel_One',
        'is_public': True,
    })
    assert res.status_code == 200
    channel = res.json()

    # Get channel details
    res = requests.get(config.url + 'channel/details/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
    })
    assert res.status_code == 200
    details = res.json()
    assert details['name'] == 'Channel_One'
    assert len(details['owner_members']) == 1
    assert len(details['all_members']) == 1

def test_http_channel_details_invalid_channel_id():
    '''
    HTTP test for channel_details for where channel id is invalid
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

    # Get channel details with invalid channel id
    res = requests.get(config.url + 'channel/details/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id']+100,
    })
    assert res.status_code == 400

def test_http_channel_details_invalid_user_id():
    '''
    HTTP test for channel_details for where user id is invalid or user is not in
    channel
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

    # Get channel details with invalid token
    res = requests.get(config.url + 'channel/details/v2', json={
        'token': owner['token']+'dog',
        'channel_id': channel['channel_id'],
    })
    assert res.status_code == 403

    # Get channel details wihen user not in channel
    res = requests.get(config.url + 'channel/details/v2', json={
        'token': member['token'],
        'channel_id': channel['channel_id'],
    })
    assert res.status_code == 403

# channel_message
def test_http_channel_message():
    '''
    HTTP test for channel_message for where all parameters are valid
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

    # Get channel messages
    res = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'start': 0,
    })
    assert res.status_code == 200
    msg = res.json()
    assert len(msg['messages']) == 1

def test_http_channel_message_invalid_channel_id():
    '''
    HTTP test for channel_message for where channel_id is invalid
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

    # Get channel messages
    res = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': 100,
        'start': 0,
    })
    assert res.status_code == 400

def test_http_channel_message_invalid_msg_idx():
    '''
    HTTP test for channel_message for where msg idx is invalid
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

    # Get channel messages
    res = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'start': 100,
    })
    assert res.status_code == 400

def test_http_channel_message_user_not_in_channel():
    '''
    HTTP test for channel_details for where user is not in the channel
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

    # Send message
    res = requests.post(config.url + 'message/send/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200

    # Get channel messages
    res = requests.get(config.url + 'channel/messages/v2', json={
        'token': member['token'],
        'channel_id': channel['channel_id'],
        'start': 0,
    })
    assert res.status_code == 403

# channel_addowner/removeowner
def test_http_channel_addowner_removeowner():
    '''
    HTTP test for channel_addowner/removeowner where all parameters are valid
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

    # User is added as owner
    res = requests.post(config.url + 'channel/addowner/v1', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': member['auth_user_id']
    })
    assert res.status_code == 200

    # Get channel details
    res = requests.get(config.url + 'channel/details/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
    })
    assert res.status_code == 200
    details = res.json()
    assert len(details['owner_members']) == 2

    res = requests.delete(config.url + 'channel/removeowner/v1', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': member['auth_user_id']
    })
    assert res.status_code == 200

    # Get channel details
    res = requests.get(config.url + 'channel/details/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
    })
    assert res.status_code == 200
    details = res.json()
    assert len(details['owner_members']) == 1

def test_http_channel_addowner_removeowner_invalid_channel_id():
    '''
    HTTP test for channel_addowner/removeowner for where channel_id is invalid
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

    # Add user as an owner
    res = requests.post(config.url + 'channel/addowner/v1', json={
        'token': owner['token'],
        'channel_id': channel['channel_id']+100,
        'u_id': member['auth_user_id']
    })
    assert res.status_code == 400

    # Removing user as owner
    res = requests.delete(config.url + 'channel/removeowner/v1', json={
        'token': owner['token'],
        'channel_id': channel['channel_id']+100,
        'u_id': member['auth_user_id']
    })
    assert res.status_code == 400

def test_http_channel_addowner_already_owner():
    '''
    HTTP test for channel_addowner for where user is already owner
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

    # Owners adds himself as owner
    res = requests.post(config.url + 'channel/addowner/v1', json={
        'token': owner['token'],
        'channel_id': channel['channel_id']+100,
        'u_id': owner['auth_user_id']
    })
    assert res.status_code == 400

def test_http_channel_addowner_removeowner_authuser_no_permission():
    '''
    HTTP test for channel_addowner/removeowner for where user has no permission
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

    # User attempts to use this route
    res = requests.post(config.url + 'channel/addowner/v1', json={
        'token': member['token'],
        'channel_id': channel['channel_id'],
        'u_id': member['auth_user_id']
    })
    assert res.status_code == 403

    # Removing owner as owner
    res = requests.delete(config.url + 'channel/removeowner/v1', json={
        'token': member['token'],
        'channel_id': channel['channel_id'],
        'u_id': owner['auth_user_id']
    })
    assert res.status_code == 403

def test_http_channel_addowner_removeowner_dreams_owner():
    '''
    HTTP test for channel_addowner/removeowner where dreams owner adds and
    removes owners
    '''
    # Resets the internal data of the application to it's initial state
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    # Register dreams owner
    res = requests.post(config.url + 'auth/register/v2', json={
        'email': 'bob.smith@gmail.com',
        'password': 'pass123',
        'name_first': 'Bob',
        'name_last': 'Smith',
    })
    assert res.status_code == 200
    dreams = res.json()

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

    # Dreams add user as owner
    res = requests.post(config.url + 'channel/addowner/v1', json={
        'token': dreams['token'],
        'channel_id': channel['channel_id'],
        'u_id': member['auth_user_id']
    })
    assert res.status_code == 200

    # Dreams removes user as owner
    res = requests.delete(config.url + 'channel/removeowner/v1', json={
        'token': dreams['token'],
        'channel_id': channel['channel_id'],
        'u_id': owner['auth_user_id']
    })
    assert res.status_code == 200

def test_http_channel_addowner_removeowner_user_not_in_channel():
    '''
    HTTP test for channel_addowner/removeowner for where user not in channel
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

    # Add user as owner
    res = requests.post(config.url + 'channel/addowner/v1', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': member['auth_user_id']
    })
    assert res.status_code == 403

    res = requests.delete(config.url + 'channel/removeowner/v1', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': member['auth_user_id']
    })
    assert res.status_code == 400

def test_http_channel_removeowner_only_owner_user_in_channel():
    '''
    HTTP test for channel_removeowner one attempts to remove the only owner or
    user is not an owner
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

    res = requests.delete(config.url + 'channel/removeowner/v1', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': owner['auth_user_id']
    })
    assert res.status_code == 400

    res = requests.delete(config.url + 'channel/removeowner/v1', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': member['auth_user_id']
    })
    assert res.status_code == 400

# channel_leave
def test_http_channel_leave():
    '''
    HTTP test for channel_leave with correct parameters
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

    # User leaves channel
    res = requests.post(config.url + 'channel/leave/v1', json={
        'token': member['token'],
        'channel_id': channel['channel_id'],
    })
    assert res.status_code == 200

    # Get channel details
    res = requests.get(config.url + 'channel/details/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
    })
    assert res.status_code == 200
    details = res.json()
    assert len(details['all_members']) == 1

def test_http_channel_leave_invalid_channel_id():
    '''
    HTTP test for channel_leave with invalid channel_id
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

    # User leaves channel
    res = requests.post(config.url + 'channel/leave/v1', json={
        'token': member['token'],
        'channel_id': channel['channel_id']+100,
    })
    assert res.status_code == 400

def test_http_channel_leave_auth_user_not_in_channel():
    '''
    HTTP test for channel_leave when auth user not in channel
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

    # User leaves channel
    res = requests.post(config.url + 'channel/leave/v1', json={
        'token': member['token'],
        'channel_id': channel['channel_id'],
    })
    assert res.status_code == 403

def test_http_channel_invite():
    """
    A simple test to check channel invite
    """

    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    new_channel = requests.post(config.url + 'channels/create/v2', json={
        "token": owner.json()['token'],
        "name": "Channel_One",
        "is_public": True
    })

    assert new_channel.status_code == 200

    user = requests.post(config.url + 'auth/register/v2', json={
        "email": "eliza.jones2@gmail.com",
        "password": "pass123",
        "name_first": "Eliza",
        "name_last": "Jones"
    })
    assert user.status_code == 200

    resp = requests.post(config.url + '/channel/invite/v2', json={
        "token": owner.json()['token'],
        "channel_id": new_channel.json()['channel_id'],
        "u_id": user.json()['auth_user_id']
    })

    assert resp.status_code == 200


def test_http_invite_channeliderror():
    """
    test channel invite input error
    channel_id not valid
    """

    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    new_channel = requests.post(config.url + 'channels/create/v2', json={
        "token": owner.json()['token'],
        "name": "Channel_One",
        "is_public": True
    })

    assert new_channel.status_code == 200

    user = requests.post(config.url + 'auth/register/v2', json={
        "email": "eliza.jones2@gmail.com",
        "password": "pass123",
        "name_first": "Eliza",
        "name_last": "Jones"
    })
    assert user.status_code == 200

    # with pytest.raises(urllib.error.HTTPError):
    res = requests.post(config.url + '/channel/invite/v2', json={
        "token": owner.json()['token'],
        "channel_id": "invalid channel id",
        "u_id": user.json()['auth_user_id']
    })
    assert res.status_code == 400

def test_http_invite_uiderror():
    """
    test channel invite input error
    u_id not valid
    """

    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    new_channel = requests.post(config.url + 'channels/create/v2', json={
        "token": owner.json()['token'],
        "name": "Channel_One",
        "is_public": True
    })

    assert new_channel.status_code == 200

    # with pytest.raises(urllib.error.HTTPError):
    res = requests.post(config.url + '/channel/invite/v2', json={
        "token": owner.json()['token'],
        "channel_id": new_channel.json()['channel_id'],
        "u_id": 20000
    })
    assert res.status_code == 400

def test_http_invite_accesserror():
    """
    test channel invite input error
    u_id already in channel
    """

    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    new_channel = requests.post(config.url + 'channels/create/v2', json={
        "token": owner.json()['token'],
        "name": "Channel_One",
        "is_public": True
    })

    assert new_channel.status_code == 200

    # with pytest.raises(urllib.error.HTTPError):
    res = requests.post(config.url + '/channel/invite/v2', json={
        "token": owner.json()['token'],
        "channel_id": new_channel.json()['channel_id'],
        "u_id": owner.json()['auth_user_id']
    })
    assert res.status_code == 403

def test_http_channel_join():
    """
    A simple test to check channel join
    """

    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    new_channel = requests.post(config.url + 'channels/create/v2', json={
        "token": owner.json()['token'],
        "name": "Channel_One",
        "is_public": True
    })

    assert new_channel.status_code == 200

    resp = requests.post(config.url + '/channel/join/v2', json={
        "token": owner.json()['token'],
        "channel_id": new_channel.json()['channel_id'],
    })
    assert resp.status_code == 200


def test_http_join_channeliderror():
    """
    test channel join input error
    channel_id not valid
    """

    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    new_channel = requests.post(config.url + 'channels/create/v2', json={
        "token": owner.json()['token'],
        "name": "Channel_One",
        "is_public": True
    })

    assert new_channel.status_code == 200

    # with pytest.raises(urllib.error.HTTPError):
    res = requests.post(config.url + '/channel/join/v2', json={
        "token": owner.json()['token'],
        "channel_id": "invalid channel id",
    })
    assert res.status_code == 400


def test_http_join_accesserror():
    """
    test channel join input error
    channel is private
    """

    # clear
    assert requests.delete(config.url + 'clear/v1').status_code == 200

    owner = requests.post(config.url + '/auth/register/v2', json={
        "email": "john.smith8@gmail.com",
        "password": "pass123",
        "name_first": "John",
        "name_last": "Smith",
    })
    assert owner.status_code == 200

    new_channel = requests.post(config.url + 'channels/create/v2', json={
        "token": owner.json()['token'],
        "name": "Channel_One",
        "is_public": False
    })

    assert new_channel.status_code == 200

    # with pytest.raises(urllib.error.HTTPError):
    res = requests.post(config.url + '/channel/join/v2', json={
        "token": owner.json()['token'],
        "channel_id": new_channel.json()['channel_id'],
    })
    assert res.status_code == 403
