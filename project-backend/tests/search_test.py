import pytest

from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError, AccessError
from src.channels import channels_create_v2
from src.other import clear_v1, search_v2
from src.dm import dm_create_v1
from src.message import message_senddm_v1, message_send_v2

def query_str_generator(characters):
    '''random string generator where the number of characters in the str'''
    query_str = ''
    counter = 0
    while counter < characters:
        query_str += str(1)
        counter += 1
    return query_str

def test_search():
    '''Test for basic functionality'''
    clear_v1()
    
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    dm = dm_create_v1(owner['token'], [member1['auth_user_id']])
    msgString = 'How are you?'
    message_senddm_v1(owner['token'], dm['dm_id'], msgString)
    
    channel = channels_create_v2(owner['token'], 'My Channel', True)
    msgString = 'How have you been'
    message_send_v2(owner['token'], channel['channel_id'], msgString)
    query_str = 'How'
    messages = search_v2(owner['token'], query_str)

    assert len(messages['messages']) == 2
    
def test_input_error():
    '''Test InputError when query_str > 1000 characters'''
    clear_v1()
    
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    results = search_v2(owner['token'], query_str_generator(1000))
    assert results == {
        'messages': [],
    }
    with pytest.raises(InputError):
        search_v2(owner['token'], query_str_generator(1001))
    
def test_invalid_token():
    '''Test for invalid token'''
    clear_v1()
    validQuery = 'hello'

    with pytest.raises(AccessError):
        search_v2(0, validQuery)
    with pytest.raises(AccessError):
        search_v2({}, validQuery)


def test_valid_token_no_messages():
    '''Test when a valid token and query_str but there are no matches'''
    clear_v1()
    
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    results = search_v2(owner['token'], 'hello')
    assert results['messages'] == []
    
