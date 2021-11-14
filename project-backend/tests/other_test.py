import pytest

from src.data import data
from src.other import clear_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.users import users_all_v1
from src.channels import channels_listall_v2


def test_clear_channels():
    '''Test if clear_v1 removes all channel entries'''

    clear_v1()

    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    channels_create_v2(owner['token'], 'My Channel 1', True)
    channels_create_v2(owner['token'], 'My Channel 2', True)

    clear_v1()

    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    channels_create_v2(owner['token'], 'My Channel 3', True)

    assert len(channels_listall_v2(owner['token'])['channels']) == 1

def test_clear_users():
    '''Test if clear_v1 removes all user entries'''

    clear_v1()

    auth_register_v2('tony.kim@gmail.com', 'pass123', 'Tony', 'Kim')
    auth_register_v2('raymond@gmail.com','pass123', 'Raymond', 'Chung')

    clear_v1()

    user = auth_register_v2('cara@gmail.com', 'pass123', 'Cara', 'Guo')

    assert len(users_all_v1(user['token'])['users']) == 1

