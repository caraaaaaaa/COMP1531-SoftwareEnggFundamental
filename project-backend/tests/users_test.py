import pytest

from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.users import users_all_v1, users_stats_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.data import data


def test_users_all_v1():
    '''test users_all_v1 function'''
    '''normal case'''
    clear_v1()
    user1 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user2 = auth_register_v2('cara.guo@gmail.com', 'pass123', 'Cara', 'Guo')
    
    users = users_all_v1(user1['token'])
    print(user2)
    for user in users['users']:
        if user['u_id'] == 1:
            assert user['email'] == 'john.johnson@gmail.com'
            assert user['password'] == 'circus123'
            assert user['name_first'] == 'John'
            assert user['name_last'] == 'Johnson'
            assert user['handle_str'] == 'john.johnson#1'
            assert user['auth_user_id'] == 1
            assert user['permission_id'] == 1
        if user['u_id'] == 2:
            assert user['email'] == 'cara.guo@gmail.com'
            assert user['password'] == 'pass123'
            assert user['name_first'] == 'Cara'
            assert user['name_last'] == 'Guo'
            assert user['handle_str'] == 'cara.guo#2'
            assert user['auth_user_id'] == 2
            assert user['permission_id'] == 2


def test_users_stats_v1():
    clear_v1()
    user1 = auth_register_v2('john.smith12@gmail.com', 'pass123', 'John', 'Smith')
    new_channel = channels_create_v2(user1['token'], 'Channel_One', True)
    user2 = auth_register_v2('john.smith4@gmail.com', 'pass123', 'Johnn', 'Smithh')
    channel_join_v2(user2['token'], new_channel['channel_id'])
    result = users_stats_v1(user2['token'])

    assert result['channels_exist'][0]['num_channels_exist'] == 1
