import pytest

from src.auth import auth_register_v2
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_join_v2
from src.channels import channels_create_v2
from src.message import message_send_v2
from src.users import users_all_v1


# Test functions for admin_user_remove_v1
def test_admin_user_remove_member():
    '''
    Testing cases for admin_user_remove_v1 with correct parameters, removing a
    member
    '''
    clear_v1()

    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(member['token'], channel['channel_id'])
    message_send_v2(member['token'], channel['channel_id'], 'Hello World')
    # dm_id = dm_create_v1(owner['token'], member['auth_user_id'])
    # message_senddm_v1(member['token'], dm_id['dm_id'], 'Hello World')
    admin_user_remove_v1(owner['token'], member['auth_user_id'])
    user_list = users_all_v1(member['token'])
    num_users = 0
    for user in user_list['users']:
        if user['name_first'] != 'Removed user':
            num_users += 1
    assert num_users == 1

    msg = channel_messages_v2(member['token'], channel['channel_id'], 0)
    assert msg['messages'][0]['message'] == 'Removed user'

    # msg = dm_messages_v1(member['token'], dm_id['dm_id'], 0)
    # assert msg['messages'][1]['message'] == 'Removed user'

def test_admin_user_remove_owner():
    '''
    Testing cases for admin_user_remove_v1 with correct parameters, removing
    another owner
    '''
    clear_v1()

    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    message_send_v2(owner['token'], channel['channel_id'], 'Hello World')
    # Member becomes an owner and removes original owner
    admin_userpermission_change_v1(owner['token'], member['auth_user_id'], 1)
    admin_user_remove_v1(member['token'], owner['auth_user_id'])
    user_list = users_all_v1(member['token'])
    num_users = 0
    for user in user_list['users']:
        if user['name_first'] != 'Removed user':
            num_users += 1
    assert num_users == 1

    msg = channel_messages_v2(owner['token'], channel['channel_id'], 0)
    assert msg['messages'][0]['message'] == 'Removed user'

def test_admin_user_remove_invalid_uid_token():
    '''
    Testing cases for admin_user_remove_v1 with an invalid u_id/token
    '''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    with pytest.raises(InputError):
        admin_user_remove_v1(owner['token'], 9)
    with pytest.raises(InputError):
        admin_user_remove_v1(owner['token'], -1)
    with pytest.raises(AccessError):
        admin_user_remove_v1(9, owner['auth_user_id'])

def test_admin_user_remove_self():
    '''
    Testing cases for admin_user_remove_v1 with owner removing himself/herself
    '''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    admin_userpermission_change_v1(owner['token'], member['auth_user_id'], 1)
    admin_user_remove_v1(owner['token'], owner['auth_user_id'])
    user_list = users_all_v1(member['token'])
    num_users = 0
    for user in user_list['users']:
        if user['name_last'] != 'Removed user':
            num_users += 1
    assert num_users == 1

def test_admin_user_remove_only_owner():
    '''
    Testing cases for admin_user_remove_v1, attempting to remove the only owner
    '''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    with pytest.raises(InputError):
        admin_user_remove_v1(owner['token'], owner['auth_user_id'])

def test_admin_user_remove_not_owner():
    '''
    Testing cases for admin_user_remove_v1 when user is not owner
    '''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    with pytest.raises(AccessError):
        admin_user_remove_v1(member['token'], owner['auth_user_id'])

# Test functions for admin_userpermission_change_v1
def test_admin_userpermission_change():
    '''
    Testing cases for admin_userpermission_change_v1 with valid parameters
    '''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    admin_userpermission_change_v1(owner['token'], member['auth_user_id'], 1)
    # Below can only be done if permissions successfully changed
    admin_user_remove_v1(member['token'], owner['auth_user_id'])

def test_admin_userpermission_change_invalid_uid_token():
    '''
    Testing cases for admin_userpermission_change_v1 with invalid uid or token
    '''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    with pytest.raises(InputError):
        admin_userpermission_change_v1(owner['token'], 9, 1)
    with pytest.raises(InputError):
        admin_userpermission_change_v1(9, owner['auth_user_id'], 1)

def test_admin_userpermission_change_invalid_permissionid():
    '''
    Testing cases for admin_userpermission_change_v1 with invalid permission id
    '''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    with pytest.raises(InputError):
        admin_userpermission_change_v1(owner['token'], member['auth_user_id'], 9)

def test_admin_userpermission_change_not_owner():
    '''
    Testing cases for admin_userpermission_change_v1 when auth user is not owner
    '''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(member['token'], owner['auth_user_id'], 2)

def test_admin_userpermission_change_same_permission():
    '''
    Testing cases for admin_userpermission_change_v1 without changing
    permissions
    '''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    admin_userpermission_change_v1(owner['token'], member['auth_user_id'], 2)
