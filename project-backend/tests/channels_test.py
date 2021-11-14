import pytest

from src.data import data
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.other import clear_v1

def test_channel_creates():
    '''
    test if a channel is added to the data dictionary by checking if the
    channel_id and name align with the newly created channel
    '''

    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    channels_create_v2(owner['token'], 'My Channel', True)

    assert channels_listall_v2(owner['token'])['channels'] == [
        {
            'channel_id' : 1,
            'name' : 'My Channel'
        }
    ]

def test_create_multiple_channels():
    '''
    test whether a newly created channel overwrites the data of the
    previously created channel
    '''

    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    channels_create_v2(owner['token'], 'My Channel 1', True)
    channels_create_v2(owner['token'], 'My Channel 2', True)

    assert channels_listall_v2(owner['token'])['channels'] == [
        {
            'channel_id' : 1,
            'name' : 'My Channel 1'
        },
        {
            'channel_id' : 2,
            'name' : 'My Channel 2'
        }
    ]

def test_create_invalid_user_id():
    '''test for when user_id input is invalid'''

    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v2(2, 'My Channel', True)
    with pytest.raises(AccessError):
        channels_create_v2('wrong', 'My Channel', True)
    with pytest.raises(AccessError):
        channels_create_v2({}, 'My Channel', True)

def test_is_public_parameter():
    '''test for when the is_public parameter is invalid'''

    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')

    with pytest.raises(InputError):
        channels_create_v2(owner['token'], 'My Channel', 'True')
    with pytest.raises(InputError):
        channels_create_v2(owner['token'], 'My Channel', 'False')
    with pytest.raises(InputError):
        channels_create_v2(owner['token'], 'My Channel', 3)
    with pytest.raises(InputError):
        channels_create_v2(owner['token'], 'My Channel', {})

def test_maximum_name():
    '''test for when name exceeds 20 characters'''

    clear_v1()

    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')

    with pytest.raises(InputError):
        channels_create_v2(owner['token'], '123456789012345678901', True)
    with pytest.raises(InputError):
        channels_create_v2(owner['token'], 'welcometothechannelxd', True)
    with pytest.raises(InputError):
        channels_create_v2(owner['token'], '!@#$%^&*()1'*2, True)


def test_channels_list():
    '''test for basic functionality'''

    clear_v1()
    owner1 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel1 = channels_create_v2(owner1['token'], 'Channel_One', True)
    channel2 = channels_create_v2(owner1['token'], 'Channel_Two', True)

    owner2 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channels_create_v2(owner2['token'], 'Channel_Three', True)

    assert channels_list_v2(owner1['token'])['channels'] == [
        {
            'channel_id' : channel1['channel_id'],
            'name' : 'Channel_One'
        },
        {
            'channel_id' : channel2['channel_id'],
            'name' : 'Channel_Two'
        }
    ]

def test_channels_listall():
    '''test for basic functionality'''

    clear_v1()
    owner1 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel1 = channels_create_v2(owner1['token'], 'Channel_One', True)
    channel2 = channels_create_v2(owner1['token'], 'Channel_Two', True)

    owner2 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channel3 = channels_create_v2(owner2['token'], 'Channel_Three', True)

    assert channels_listall_v2(owner1['token'])['channels'] == [
        {
            'channel_id' : channel1['channel_id'],
            'name' : 'Channel_One'
        },
        {
            'channel_id' : channel2['channel_id'],
            'name' : 'Channel_Two'
        },
        {
            'channel_id' : channel3['channel_id'],
            'name' : 'Channel_Three'
        }
    ]

def test_channels_list_private():
    '''test for private list'''

    clear_v1()
    owner1 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel1 = channels_create_v2(owner1['token'], 'Channel_One', True)
    channel2 = channels_create_v2(owner1['token'], 'Channel_Two', False)

    owner2 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channels_create_v2(owner2['token'], 'Channel_Three', False)

    assert channels_list_v2(owner1['token'])['channels'] == [
        {
            'channel_id' : channel1['channel_id'],
            'name' : 'Channel_One'
        },
        {
            'channel_id' : channel2['channel_id'],
            'name' : 'Channel_Two'
        }
    ]

def test_channels_listall_private():
    '''test for private list'''

    clear_v1()
    owner1 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel1 = channels_create_v2(owner1['token'], 'Channel_One', True)
    channel2 = channels_create_v2(owner1['token'], 'Channel_Two', False)

    owner2 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channel3 = channels_create_v2(owner2['token'], 'Channel_Three', False)

    assert channels_listall_v2(owner1['token'])['channels'] == [
        {
            'channel_id' : channel1['channel_id'],
            'name' : 'Channel_One'
        },
        {
            'channel_id' : channel2['channel_id'],
            'name' : 'Channel_Two'
        },
        {
            'channel_id' : channel3['channel_id'],
            'name' : 'Channel_Three'
        }
    ]

def test_channels_list_empty():
    '''test for empty list'''

    clear_v1()
    owner1 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')

    assert channels_list_v2(owner1['token'])['channels'] == []

def test_channels_listall_empty():
    '''test for empty list'''

    clear_v1()
    owner1 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')

    assert channels_listall_v2(owner1['token'])['channels'] == []

def test_channels_list_input_error():
    '''test for invalid user id'''

    clear_v1()

    with pytest.raises(AccessError):
        channels_list_v2([])

def test_channels_listall_input_error():
    '''test for invalid user id'''

    clear_v1()
    auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')

    with pytest.raises(AccessError):
        channels_listall_v2([])
