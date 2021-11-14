import pytest
import requests
import json
from src import config

def test_http_admin_user_remove_member():
    '''
    HTTP test for admin_user_remove for where all parameters are valid,
    removing a member
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

    # User sends a message in channel
    res = requests.post(config.url + 'message/send/v2', json={
        'token': member['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello World',
    })
    assert res.status_code == 200

    # Owner removes user from Dreams
    res = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': owner['token'],
        'u_id': member['auth_user_id'],
    })
    assert res.status_code == 200

    # Retreieves list of users and checks name has been changed to 'Removed User'
    res = requests.get(config.url + 'users/all/v1', json={
        'token': owner['token']
    })
    payload = res.json()
    assert payload['users'][1]['name_first'] == 'Removed user'

    # Retreieves list of messages and checks messages has been changed
    # to 'Removed User'
    res = requests.get(config.url + 'channel/messages/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'start': 0,
    })
    payload = res.json()
    assert payload['messages'][0]['message'] == 'Removed user'

def test_http_admin_user_remove_invalid_uid_token():
    '''
    HTTP test for admin_user_remove for where all the u_id/token is invalid
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

    # Inputting invalid u_id
    res = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': owner['token'],
        'u_id': 9,
    })
    assert res.status_code == 400

    # Inputting invalid token
    res = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': 9,
        'u_id': owner['auth_user_id'],
    })
    assert res.status_code == 403

def test_http_admin_user_remove_only_owner():
    '''
    HTTP test for admin_user_remove for where one attempts to remove the only
    owner
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

    # Removing only owner
    res = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': owner['token'],
        'u_id': owner['auth_user_id'],
    })
    assert res.status_code == 400

def test_http_admin_user_remove_not_owner():
    '''
    HTTP test for admin_user_remove for where one attempts to use this route
    without the required permissions
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

    # User trying to remove owner
    res = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': member['token'],
        'u_id': owner['auth_user_id'],
    })
    assert res.status_code == 403

def test_http_admin_userpermission_change():
    '''
    HTTP test for admin_userpermission_change for where all parameters are valid,
    removing a member
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

    # Changing member's permission to owner
    res = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': owner['token'],
        'u_id': member['auth_user_id'],
        'permission_id': 1
    })
    assert res.status_code == 200

    # Member should now have permision to remove owner
    res = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': member['token'],
        'u_id': owner['auth_user_id'],
    })
    assert res.status_code == 200

def test_http_admin_userpermission_change_invalid_uid_token():
    '''
    HTTP test for admin_userpermission_change for where u_id/token is invalid
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

    # Changing member's permission to owner with invalid member u_id
    res = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': owner['token'],
        'u_id': 9,
        'permission_id': 1
    })
    assert res.status_code == 400

    # Changing member's permission to owner with invalid owner token
    res = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': 9,
        'u_id': owner['auth_user_id'],
        'permission_id': 1
    })
    assert res.status_code == 400

def test_http_admin_userpermission_change_invalid_permission_id():
    '''
    HTTP test for admin_userpermission_change for where permission_id is invalid
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

    # Changing member's permission to owner with invalid permission id
    res = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': owner['token'],
        'u_id': member['auth_user_id'],
        'permission_id': 9
    })
    assert res.status_code == 400

def test_http_admin_userpermission_change_not_owner():
    '''
    HTTP test for admin_userpermission_change for where one attempts to use
    this route without the required permissions
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

    # Member should not have permision to remove owner
    res = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': member['token'],
        'u_id': owner['auth_user_id'],
    })
    assert res.status_code == 403

def test_http_admin_userpermission_change_same_permission():
    '''
    HTTP test for admin_userpermission_change for where the permission is not
    changed
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

    # Making no changes, should have no errors
    res = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': owner['token'],
        'u_id': member['auth_user_id'],
        'permission_id': 2
    })
    assert res.status_code == 200
