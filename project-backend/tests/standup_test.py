import pytest
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1, time_finder
from src.channels import channels_create_v2
from src.channel import channel_invite_v2, channel_messages_v2
from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import InputError, AccessError
from datetime import datetime
from time import sleep

'''PYTEST FIXTURES'''
@pytest.fixture
def user1():
    clear_v1()
    user1 = auth_register_v2('one@gmail.com', 'password', 'one', 'name')
    return user1

@pytest.fixture
def user2():
    user2 = auth_register_v2('two@gmail.com', 'password', 'two', 'name')
    return user2

@pytest.fixture
def user3():
    user3 = auth_register_v2('three@gmail.com', 'password', 'three', 'name')
    return user3


'''TESTS FOR STANDUP FUNCTIONS'''
def test_basic_standup_start(user1):
    '''Test basic functionality of standup_start_v1 function'''
    channel = channels_create_v2(user1['token'], 'Channel1', True)
    standup = standup_start_v1(user1['token'], channel['channel_id'], 5)
    assert standup == {
        'time_finish': time_finder(channel['channel_id'])
    }
    status = standup_active_v1(user1['token'], channel['channel_id'])
    assert status['is_active'] == True
    
def test_start_invalid_token(user1, user2, user3):
    '''Test for invalid token'''
    channel = channels_create_v2(user1['token'], 'Channel1', True)
    with pytest.raises(AccessError):
        standup_start_v1(user2['token'], channel['channel_id'], 5)
    with pytest.raises(AccessError):
        standup_start_v1(user3['token'], channel['channel_id'], 5)
    with pytest.raises(AccessError):
        standup_start_v1(0, channel['channel_id'], 5)
    with pytest.raises(AccessError):
        standup_start_v1({}, channel['channel_id'], 5)
    
def test_start_invalid_channel_id(user1):
    '''Test for invalid channel id'''
    channels_create_v2(user1['token'], 'Channel1', True)
    with pytest.raises(InputError):
        standup_start_v1(user1['token'], {}, 5)
    with pytest.raises(InputError):
        standup_start_v1(user1['token'], 'wrong', 5)
    with pytest.raises(InputError):
        standup_start_v1(user1['token'], 0, 5)
    
def test_start_already_active_standup(user1):
    '''Test for when a standup is already in session'''
    channel = channels_create_v2(user1['token'], 'Channel1', True)
    standup_start_v1(user1['token'], channel['channel_id'], 5)
    with pytest.raises(InputError):
        standup_start_v1(user1['token'], channel['channel_id'], 5)

def test_standup_active_v1(user1):
    '''Test basic functionality of standup_active_v1'''
    channel = channels_create_v2(user1['token'], 'Channel1', True)
    standup = standup_active_v1(user1['token'], channel['channel_id'])
    assert standup == {
        'time_finish': None,
        'is_active': False,
    }
    standup_start_v1(user1['token'], channel['channel_id'], 10)
    standup = standup_active_v1(user1['token'], channel['channel_id'])
    assert standup == {
        'is_active': True,
        'time_finish': time_finder(channel['channel_id'])
    }

def test_active_invalid_token(user1, user2, user3):
    '''Test for invalid token'''
    channel = channels_create_v2(user1['token'], 'Channel1', True)
    with pytest.raises(AccessError):
        standup_active_v1(0, channel['channel_id'])
    with pytest.raises(AccessError):
        standup_active_v1({}, channel['channel_id'])
    with pytest.raises(AccessError):
        standup_active_v1(user2['token'], channel['channel_id'])
    with pytest.raises(AccessError):
        standup_active_v1(user3['token'], channel['channel_id'])
    
def test_active_invalid_channel_id(user1):
    '''Test for invalid channel id'''
    channels_create_v2(user1['token'], 'Channel1', True)
    with pytest.raises(InputError):
        standup_active_v1(user1['token'], {})
    with pytest.raises(InputError):
        standup_active_v1(user1['token'], 'wrong')
    with pytest.raises(InputError):
        standup_active_v1(user1['token'], 0)

def test_standup_send_v1(user1, user2, user3):
    '''Test basic functionality of standup_send_v1'''
    channel = channels_create_v2(user1['token'], 'Channel1', True)
    channel_invite_v2(user1['token'], channel['channel_id'], user2['auth_user_id'])
    channel_invite_v2(user1['token'], channel['channel_id'], user3['auth_user_id'])
    standup_start_v1(user1['token'], channel['channel_id'], 5)
    standup = standup_send_v1(user1['token'], channel['channel_id'], 'hello')
    assert standup == {}
    
    standup_send_v1(user2['token'], channel['channel_id'], 'hello')
    standup_send_v1(user3['token'], channel['channel_id'], 'hello')
    sleep(5)
    messages = channel_messages_v2(user1['token'], channel['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'one: hello\n'+'two: hello\n'+'three: hello'
    
def test_send_invalid_token(user1, user2, user3):
    '''Test for invalid token'''
    channel = channels_create_v2(user1['token'], 'Channel1', True)
    standup_start_v1(user1['token'], channel['channel_id'], 5)
    with pytest.raises(AccessError):
        standup_send_v1(0, channel['channel_id'], 'hello')
    with pytest.raises(AccessError):
        standup_send_v1({}, channel['channel_id'], 'hello')
    with pytest.raises(AccessError):
        standup_send_v1(user2['token'], channel['channel_id'], 'hello')
    with pytest.raises(AccessError):
        standup_send_v1(user3['token'], channel['channel_id'], 'hello')

def test_send_invalid_channel_id(user1):
    '''Test for invalid channel_id'''
    channel = channels_create_v2(user1['token'], 'Channel1', True)
    standup_start_v1(user1['token'], channel['channel_id'], 5)
    with pytest.raises(InputError):
        standup_send_v1(user1['token'], 0, 'hello')
    with pytest.raises(InputError):
        standup_send_v1(user1['token'], '1', 'hello')
    with pytest.raises(InputError):
        standup_send_v1(user1['token'], {}, 'hello')

def test_send_invalid_message(user1):
    '''Test for invalid message'''
    channel = channels_create_v2(user1['token'], 'Channel1', True)
    message = message_generator(1000)
    standup_start_v1(user1['token'], channel['channel_id'], 10)
    standup_send_v1(user1['token'], channel['channel_id'], message)
    message = message_generator(1001)
    with pytest.raises(InputError):
        standup_send_v1(user1['token'], channel['channel_id'], message)

def test_send_standup_inactive(user1):
    '''Test when a standup is inactive'''
    channel = channels_create_v2(user1['token'], 'Channel1', True)
    with pytest.raises(InputError):
        standup_send_v1(user1['token'], channel['channel_id'], 'hello')
    
'''HELPER FUNCTIONS'''
def message_generator(length):
    emptyString = ''
    counter = 0
    while counter < length:
        emptyString += '1'
        counter += 1
    if len(emptyString) == length:
        return emptyString
