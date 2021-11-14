import pytest

from src.auth import auth_register_v2
from src.error import InputError
from src.error import AccessError
from src.channel import channel_messages_v2, channel_join_v2
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.message import message_edit_v2, message_remove_v1, message_send_v2, message_senddm_v1, message_share_v1, message_sendlater_v1, message_sendlaterdm_v1, message_react_v1, message_pin_v1, message_unpin_v1, message_unreact_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_messages_v1
from datetime import datetime
from time import sleep

def test_message_send_v2():
    '''testing message send with correct parameters'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)

    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")
    message_list = channel_messages_v2(owner['token'], channel_1['channel_id'], 0)
    assert message1_id == 1
    assert message_list['messages'][0]['message'] == "Hello World!"

def test_message_send_input_error():
    '''testing message send with message over 1000 in length'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)

    with pytest.raises(InputError):
        message_send_v2(owner['token'], channel_1['channel_id'], 1001*"h")

def test_message_send_access_error():
    '''testing message send with invalid user'''
    clear_v1()
    owner = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)

    with pytest.raises(AccessError):
        message_send_v2('dog', channel_1['channel_id'], "Hello!")

def test_message_edit_v2():
    '''testing message edit with correct parameters'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")

    message_edit_v2(owner['token'], message1_id, "Goodbye World...")
    message_list = channel_messages_v2(owner['token'], channel_1['channel_id'], 0)
    assert message1_id == 1
    assert message_list['messages'][0]['message'] == "Goodbye World..."

def test_message_edit_empty():
    '''testing message edit with empty message'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")

    message_edit_v2(owner['token'], message1_id, "")
    message_list = channel_messages_v2(owner['token'], channel_1['channel_id'], 0)
    assert len(message_list['messages']) == 0


def test_message_edit_input_error_length():
    '''testing message edit with message over 1000 in length'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")

    with pytest.raises(InputError):
        message_edit_v2(owner['token'], message1_id, 1001*"h")

def test_message_edit_input_error_deleted():
    '''testing message edit on deleted message'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")
    message_edit_v2(owner['token'], message1_id, "")

    with pytest.raises(InputError):
        message_edit_v2(owner['token'], message1_id, "Hello!")

def test_message_edit_access_error():
    '''testing message edit with a user who didn't send the message nor owns the channel'''
    clear_v1()
    owner = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user1 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user2 = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')

    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user1['token'], channel_1['channel_id'])
    channel_join_v2(user2['token'], channel_1['channel_id'])

    message1_id = message_send_v2(user1['token'], channel_1['channel_id'], "Hello World!")

    with pytest.raises(AccessError):
        message_edit_v2(user2['token'], message1_id, "Hello Circus!")
    with pytest.raises(AccessError):
        message_edit_v2('dog', message1_id, "Hello Circus!")
def test_message_remove_v1():
    '''test message remove basic functionallity'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")

    message_remove_v1(owner['token'], message1_id)
    message_list = channel_messages_v2(owner['token'], channel_1['channel_id'], 0)
    assert len(message_list['messages']) == 0


def test_message_remove_deleted():
    '''testing message remove on deleted message'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")
    message_remove_v1(owner['token'], message1_id)

    with pytest.raises(InputError):
        message_remove_v1(owner['token'], message1_id)

def test_message_remove_access_error():
    '''testing message remove with a user who didn't send the message nor owns the channel'''
    clear_v1()
    owner = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user1 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user2 = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')

    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user1['token'], channel_1['channel_id'])
    channel_join_v2(user2['token'], channel_1['channel_id'])

    message1_id = message_send_v2(user1['token'], channel_1['channel_id'], "Hello World!")

    with pytest.raises(AccessError):
        message_remove_v1(user2['token'], message1_id)
    with pytest.raises(AccessError):
        message_remove_v1('dog', message1_id)

def test_message_share_v1_channel():
    '''test message share basic functionallity'''
    clear_v1()
    owner = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_2 = channels_create_v2(owner['token'], 'Channel_Two', True)

    message_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")
    message_share_v1(owner['token'], message_id, "Wow!", channel_2['channel_id'], -1)
    message_list = channel_messages_v2(owner['token'], channel_2['channel_id'], 0)
    assert message_list['messages'][0]['message'] == '"Hello World!"\nWow!'

def test_message_share_v1_no_option():
    '''test message share without an additional message'''
    clear_v1()
    owner = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_2 = channels_create_v2(owner['token'], 'Channel_Two', True)

    message_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")
    message_share_v1(owner['token'], message_id, "", channel_2['channel_id'], -1)
    message_list = channel_messages_v2(owner['token'], channel_2['channel_id'], 0)
    assert message_list['messages'][0]['message'] == '"Hello World!"'

def test_message_share_v1_access_error():
    '''test message share when user tries to share to a channel they aren't in'''
    clear_v1()
    owner1 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    owner2 = auth_register_v2('John.Johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner1['token'], 'Channel_One', True)
    channel_2 = channels_create_v2(owner2['token'], 'Channel_Two', True)

    message_id = message_send_v2(owner1['token'], channel_1['channel_id'], "Hello World!")
    with pytest.raises(AccessError):
        message_share_v1(owner1['token'], message_id, "Wow!", channel_2['channel_id'], -1)

def test_message_share_v1_dm():
    '''test message share basic functionallity in a dm'''
    clear_v1()
    user1 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user3 = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    dm2 = dm_create_v1(user1['token'], [user3['auth_user_id']])

    message_id = message_senddm_v1(user2['token'], dm1['dm_id'], "Hello World!")
    message_share_v1(user1['token'], message_id, "Get a load of this guy!", -1, dm2['dm_id'])
    message_list = dm_messages_v1(user1['token'], dm2['dm_id'], 0)
    assert message_list['messages'][0]['message'] == '"Hello World!"\nGet a load of this guy!'

def test_message_share_v1_dm_no_option():
    '''test message share in a dm with no additional message'''
    clear_v1()
    user1 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user3 = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    dm2 = dm_create_v1(user1['token'], [user3['auth_user_id']])

    message_id = message_senddm_v1(user2['token'], dm1['dm_id'], "Hello World!")
    message_share_v1(user1['token'], message_id, "", -1, dm2['dm_id'])
    message_list = dm_messages_v1(user1['token'], dm2['dm_id'], 0)
    assert message_list['messages'][0]['message'] == '"Hello World!"'

def test_message_share_v1_dm_access_error():
    '''test message share in a dm which user does not have access to'''
    clear_v1()
    user1 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user3 = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    dm2 = dm_create_v1(user1['token'], [user3['auth_user_id']])

    message_id = message_senddm_v1(user1['token'], dm1['dm_id'], "Hello World!")

    with pytest.raises(AccessError):
        message_share_v1(user2['token'], message_id, "", -1, dm2['dm_id'])

def test_message_senddm_v1():
    '''testing dm message send with correct parameters'''
    clear_v1()
    user1 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])

    message_id = message_senddm_v1(user1['token'], dm1['dm_id'], "Hello World!")
    message_list = dm_messages_v1(user1['token'], dm1['dm_id'], 0)
    assert message_id == 1
    assert message_list['messages'][0]['message'] == "Hello World!"

def test_message_senddm_input_error():
    '''testing dm message send with message length greater than 1000'''
    clear_v1()
    user1 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])

    with pytest.raises(InputError):
        message_senddm_v1(user1['token'], dm1['dm_id'], 1001*"h")

def test_message_senddm_access_error():
    '''testing dm message send with user outside of dm'''
    clear_v1()
    user1 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user3 = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])

    with pytest.raises(AccessError):
        message_senddm_v1(user3['token'], dm1['dm_id'], "hehexd")

def test_message_sendlater():
    '''testing message send later for basic functionallity'''

    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    send_time = datetime.timestamp(datetime.now()) + 2

    message_sendlater_v1(owner['token'], channel_1['channel_id'], "Hello World!", send_time)
    message_list = channel_messages_v2(owner['token'], channel_1['channel_id'], 0)
    assert len(message_list['messages']) == 0

    sleep(3)
    message_list = channel_messages_v2(owner['token'], channel_1['channel_id'], 0)
    assert len(message_list['messages']) == 1

def test_message_sendlater_input_error():
    '''testing message send later for Input Error'''

    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)

    #time is in the past
    send_time = datetime.timestamp(datetime.now()) - 2
    with pytest.raises(InputError):
        message_sendlater_v1(owner['token'], channel_1['channel_id'], "Hello World!", send_time)

    #invalid channel
    send_time = datetime.timestamp(datetime.now()) + 2
    with pytest.raises(InputError):
        message_sendlater_v1(owner['token'], 50, "Hello World!", send_time)

    #invalid message length
    send_time = datetime.timestamp(datetime.now()) + 2
    with pytest.raises(InputError):
        message_sendlater_v1(owner['token'], channel_1['channel_id'], 1001*'h', send_time)

def test_message_sendlater_access_error():
    '''testing message send later for Access Error'''

    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    user = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')

    send_time = datetime.timestamp(datetime.now()) + 2
    #user not in channel
    with pytest.raises(AccessError):
        message_sendlater_v1(user['token'], channel_1['channel_id'], "Hello World!", send_time)

def test_message_sendlaterdm_v1():
    '''testing message send later dm with correct parameters'''
    clear_v1()
    user1 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    send_time = datetime.timestamp(datetime.now()) + 2

    message_sendlaterdm_v1(user1['token'], dm1['dm_id'], "Hello World!", send_time)
    message_list = dm_messages_v1(user1['token'], dm1['dm_id'], 0)
    assert len(message_list['messages']) == 0

    sleep(3)
    message_list = dm_messages_v1(user1['token'], dm1['dm_id'], 0)
    assert len(message_list['messages']) == 1

def test_message_sendlaterdm_input_error():
    '''testing message send later dm for input error'''
    clear_v1()
    user1 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])

    #time is in the past
    send_time = datetime.timestamp(datetime.now()) - 2
    with pytest.raises(InputError):
        message_sendlaterdm_v1(user1['token'], dm1['dm_id'], "Hello World!", send_time)

    #invalid channel
    send_time = datetime.timestamp(datetime.now()) + 2
    with pytest.raises(InputError):
        message_sendlaterdm_v1(user1['token'], 50, "Hello World!", send_time)

    #invalid message length
    send_time = datetime.timestamp(datetime.now()) + 2
    with pytest.raises(InputError):
        message_sendlaterdm_v1(user1['token'], dm1['dm_id'], 1001*'h', send_time)

def test_message_sendlaterdm_access_error():
    '''testing message send later dm for access error'''
    clear_v1()
    user1 = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user3 = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])

    #user not in dm
    send_time = datetime.timestamp(datetime.now()) + 2
    with pytest.raises(AccessError):
        message_sendlaterdm_v1(user3['token'], dm1['dm_id'], "Hello World!", send_time)

def test_message_react_v1():
    '''testing message react for basic functionallity'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel_1['channel_id'])
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")

    message_react_v1(user['token'], message1_id, 1)
    message_list = channel_messages_v2(owner['token'], channel_1['channel_id'], 0)
    assert message_list['messages'][0]['reacts'][0]['react_id'] == 1
    assert message_list['messages'][0]['reacts'][0]['u_ids'] == [user['auth_user_id']]

def test_message_react_input_error():
    '''testing message react for input error'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel_1['channel_id'])
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")

    #with incorrect message id
    with pytest.raises(InputError):
        message_react_v1(user['token'], 3, 1)

    #react id is invalid (in this situation only valid is 1)
    with pytest.raises(InputError):
        message_react_v1(user['token'], message1_id, 3)

    #user had already reacted to message
    message_react_v1(user['token'], message1_id, 1)
    with pytest.raises(InputError):
        message_react_v1(user['token'], message1_id, 1)

def test_message_react_access_error():
    '''testing message react for access error'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel_1['channel_id'])
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")

    #user is not a member of channel
    with pytest.raises(AccessError):
        message_react_v1(user2['token'], message1_id, 1)

def test_message_unreact_v1():
    '''testing message react for basic functionallity'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel_1['channel_id'])
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")

    message_react_v1(user['token'], message1_id, 1)
    message_unreact_v1(user['token'], message1_id, 1)
    message_list = channel_messages_v2(owner['token'], channel_1['channel_id'], 0)
    assert len(message_list['messages'][0]['reacts']) == 0

def test_message_unreact_input_error():
    '''testing message react for input error'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel_1['channel_id'])
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")
    message_react_v1(user['token'], message1_id, 1)
    #with incorrect message id
    with pytest.raises(InputError):
        message_unreact_v1(user['token'], 3, 1)

    #react id is invalid (in this situation only valid is 1)
    with pytest.raises(InputError):
        message_unreact_v1(user['token'], message1_id, 3)

    #user had already unreacted to message
    message_unreact_v1(user['token'], message1_id, 1)
    with pytest.raises(InputError):
        message_unreact_v1(user['token'], message1_id, 1)

def test_message_unreact_access_error():
    '''testing message react for access error'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel_1['channel_id'])
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")
    message_react_v1(user['token'], message1_id, 1)
    #user is not a member of channel
    with pytest.raises(AccessError):
        message_unreact_v1(user2['token'], message1_id, 1)

def test_message_pin():
    '''testing if message can be pinned with correct variables'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel_1['channel_id'])
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")
    message_pin_v1(owner['token'], message1_id)
    message_list = channel_messages_v2(owner['token'], channel_1['channel_id'], 0)
    assert message_list['messages'][0]['is_pinned'] == True

    dm = dm_create_v1(owner['token'], [user['auth_user_id']])
    message2_id = message_senddm_v1(owner['token'], dm['dm_id'], "Hello World!")
    message_pin_v1(owner['token'], message2_id)
    message_list = dm_messages_v1(owner['token'], dm['dm_id'], 0)
    assert message_list['messages'][0]['is_pinned'] == True

def test_message_pin_input_error():
    '''testing message can be pinned for input errors'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")

    # invalid msg id
    with pytest.raises(InputError):
        message_pin_v1(owner['token'], message1_id+100)

    message_pin_v1(owner['token'], message1_id)
    # msg already pinned
    with pytest.raises(InputError):
        message_pin_v1(owner['token'], message1_id)


def test_message_pin_access_error():
    '''testing message can be pinned for access errors'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")
    dm = dm_create_v1(owner['token'], [user['auth_user_id']])
    message2_id = message_senddm_v1(owner['token'], dm['dm_id'], "Hello World!")

    # user not in channel
    with pytest.raises(AccessError):
        message_pin_v1(user['token'], message1_id)
    # user not in dm
    with pytest.raises(AccessError):
        message_pin_v1(user2['token'], message2_id)

    channel_join_v2(user['token'], channel_1['channel_id'])

    # Auth user not owner
    with pytest.raises(AccessError):
        message_pin_v1(user['token'], message1_id)
    with pytest.raises(AccessError):
        message_pin_v1(user['token'], message2_id)

def test_message_unpin():
    '''testing if message can be pinned with correct variables'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel_1['channel_id'])
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")
    message_pin_v1(owner['token'], message1_id)
    message_unpin_v1(owner['token'], message1_id)
    message_list = channel_messages_v2(owner['token'], channel_1['channel_id'], 0)
    assert message_list['messages'][0]['is_pinned'] == False

    dm = dm_create_v1(owner['token'], [user['auth_user_id']])
    message2_id = message_senddm_v1(owner['token'], dm['dm_id'], "Hello World!")
    message_pin_v1(owner['token'], message2_id)
    message_unpin_v1(owner['token'], message2_id)
    message_list = dm_messages_v1(owner['token'], dm['dm_id'], 0)
    assert message_list['messages'][0]['is_pinned'] == False

def test_message_unpin_input_error():
    '''testing message can be pinned for input errors'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")

    # invalid msg id
    with pytest.raises(InputError):
        message_pin_v1(owner['token'], message1_id)
        message_unpin_v1(owner['token'], message1_id+100)

    message_unpin_v1(owner['token'], message1_id)
    # msg already unpinned
    with pytest.raises(InputError):
        message_unpin_v1(owner['token'], message1_id)


def test_message_unpin_access_error():
    '''testing message can be pinned for access errors'''
    clear_v1()
    owner = auth_register_v2('john.johnson@gmail.com', 'circus123', 'John', 'Johnson')
    user = auth_register_v2('steve.longson@gmail.com', 'zap123', 'Steve', 'Longson')
    user2 = auth_register_v2('ethan.ethanson@gmail.com', 'monke123', 'Ethan', 'Ethanson')
    channel_1 = channels_create_v2(owner['token'], 'Channel_One', True)
    message1_id = message_send_v2(owner['token'], channel_1['channel_id'], "Hello World!")
    dm = dm_create_v1(owner['token'], [user['auth_user_id']])
    message2_id = message_senddm_v1(owner['token'], dm['dm_id'], "Hello World!")

    # user not in channel
    message_pin_v1(owner['token'], message1_id)
    message_pin_v1(owner['token'], message2_id)
    with pytest.raises(AccessError):
        message_unpin_v1(user['token'], message1_id)
    # user not in dm
    with pytest.raises(AccessError):
        message_unpin_v1(user2['token'], message2_id)

    channel_join_v2(user['token'], channel_1['channel_id'])

    # Auth user not owner
    with pytest.raises(AccessError):
        message_unpin_v1(user['token'], message1_id)
    with pytest.raises(AccessError):
        message_unpin_v1(user['token'], message2_id)