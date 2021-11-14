
import pytest

from src.channel import channel_invite_v2, channel_join_v2, user_finder, channel_details_v2, channel_messages_v2, channel_removeowner_v1, channel_addowner_v1, channel_leave_v1
from src.channels import channels_create_v2
from src.other import clear_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.data import data
from src.message import message_send_v2


# # test channel_invite channel id InputError
# def test_channel_invite_v1_channel_inputError():
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     user1 = auth_register_v1('hayden.everest@gmail.com', '123abc', 'Hayden', 'Everest')
#     user2 = auth_register_v1('hayden2.everest@gmail.com', '123abc', 'Hayden', 'Everest')
#     user3 = auth_register_v1('hayden3.everest@gmail.com', '123abc', 'Hayden', 'Everest')
#     invalid_channel_id = 300

#     with pytest.raises(InputError):
#         channel_invite_v1(owner['auth_user_id'], invalid_channel_id, user1['auth_user_id'])
#     with pytest.raises(InputError):
#         channel_invite_v1(owner['auth_user_id'], "ThisIsAString", user2['auth_user_id'])
#     with pytest.raises(InputError):
#         channel_invite_v1(owner['auth_user_id'], '1', user3['auth_user_id'])


# # test user id inputError
# def test_channel_invite_v1_user_inputError():
#     clear_v1()
#     user1 = auth_register_v1('john1.smith@gmail.com', 'pass123', 'John', 'Smith')
#     user2 = auth_register_v1('hayden4.everest@gmail.com', '123abc', 'Hayden', 'Everest')
#     user3 = auth_register_v1('hayden5.everest@gmail.com', '123abc', 'Hayden', 'Everest')
#     channel = channels_create_v1(user1['auth_user_id'], 'Channel_One', True)
#     invalid_u_id = 200

#     with pytest.raises(InputError):
#         channel_invite_v1(user1['auth_user_id'], channel['channel_id'], invalid_u_id)
#     with pytest.raises(InputError):
#         channel_invite_v1(user2['auth_user_id'], channel['channel_id'], "ThisIsAString")
#     with pytest.raises(InputError):
#         channel_invite_v1(user3['auth_user_id'], channel['channel_id'], "1")



# # test Access Error (member is already in channel)
# def test_channel_invite_v1_accessError():
#     clear_v1()
#     auth_register_v1('john.smith2@gmail.com', 'pass123', 'John', 'Smith')
#     user4 = auth_register_v1('hayden6.everest@gmail.com', '123abc', 'Hayden', 'Everest')
#     # channel = {'channels': [
#     #     {
#     #         'id': 1,
#     #         'name' : 'Channel_One',
#     #     },
#     #     {
#     #         'id': 2,
#     #         'name' : 'channel2',
#     #     },
#     # ]
#     # }
#     # unused variable, commented out

#     with pytest.raises(InputError):
#         channel_invite_v1(user4['auth_user_id'], 1, "1")

# # test channel_join channel id InputError
# def test_channel_join_v1_channel_inputError():
#     clear_v1()
#     owner2 = auth_register_v1('john.smith3@gmail.com', 'pass123', 'John', 'Smith')
#     owner3 = auth_register_v1('john.smith4@gmail.com', 'pass123', 'John', 'Smith')
#     owner4 = auth_register_v1('john.smith5@gmail.com', 'pass123', 'John', 'Smith')
#     invalid_channel_id = 400

#     with pytest.raises(InputError):
#         channel_join_v1(owner2['auth_user_id'], invalid_channel_id)
#     with pytest.raises(InputError):
#         channel_join_v1(owner3['auth_user_id'], "ThisIsAString")
#     with pytest.raises(InputError):
#         channel_join_v1(owner4['auth_user_id'], '1')


# # test Access Error (member is already in channel)
# def test_channel_join_v1_accessError():
#     clear_v1()
#     owner = auth_register_v1('john.smith6@gmail.com', 'pass123', 'John', 'Smith')
#     channel = channels_create_v1(owner['auth_user_id'], 'Channel_Seven', False)
#     auth_register_v1('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')

#     with pytest.raises(InputError):
#         channel_join_v1(owner['auth_user_id'], channel['channel_id'])

# # test join
# def test_channel_join_v1():
#     clear_v1()
#     owner11 = auth_register_v1('john.smith12@gmail.com', 'pass123', 'John', 'Smith')
#     newchannel = channels_create_v1(owner11['auth_user_id'], 'Channel_One', True)

#     # calculate the number of members in the channel
#     len1 = 0
#     for channel in data['channels']:
#         if channel['channel_id'] == newchannel['channel_id']:
#             len1 = len(channel['all_members'])
#             print(channel['all_members'])

#     # run the channel_join_v1 function
#     channel_join_v1(owner11['auth_user_id'], newchannel['channel_id'])

#     # calculate the number of members in the channel
#     len2 = 0
#     for channel in data['channels']:
#         print(channel['all_members'])
#         if channel['channel_id'] == newchannel['channel_id']:
#             len2 = len(channel['all_members'])

#     # join function been called once, so number of members will 1 more than before
#     assert (len2 - len1) == 1

# # test invite
# def test_channel_invite_v1():
#     clear_v1()
#     # create new member and new channel
#     owner = auth_register_v1('john.smith8@gmail.com', 'pass123', 'John', 'Smith')
#     newchannel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)
#     user = auth_register_v1('eliza.jones2@gmail.com', 'pass123', 'Eliza', 'Jones')

#     # calculate the number of members in the channel
#     len1 = 0
#     for channel in data['channels']:
#         if channel['channel_id'] == newchannel['channel_id']:
#             len1 = len(channel['all_members'])
#             print(channel['all_members'])

#     # run the channel_invite_v1 function
#     channel_invite_v1(owner['auth_user_id'], newchannel['channel_id'], user['auth_user_id'])

#     # calculate the number of members in the channel
#     len2 = 0
#     for channel in data['channels']:
#         print(channel['all_members'])
#         if channel['channel_id'] == newchannel['channel_id']:
#             len2 = len(channel['all_members'])

#     # invite function been called once, so number of members will 1 more than before
#     assert (len2 - len1) == 1



# # @pytest.fixture
# # def channel_setup():
# #     clear_v1()
# #     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
# #     channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)

# def test_channel_details_v1():
#     '''Testings cases for channel_details_v1 with correct parameters'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)

#     details = channel_details_v1(owner['auth_user_id'], channel['channel_id'])
#     assert details['name'] == 'Channel_One'
#     assert len(details['owner_members']) == 1
#     assert len(details['all_members']) == 1

# def test_details_invalid_channel_id():
#     '''Requesting channel details with invalid channel id'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')

#     invalid_channel_id = 2

#     with pytest.raises(InputError):
#         channel_details_v1(owner['auth_user_id'], invalid_channel_id)
#     with pytest.raises(InputError):
#         channel_details_v1(owner['auth_user_id'], "ThisIsAString")
#     with pytest.raises(InputError):
#         channel_details_v1(owner['auth_user_id'], '1')

# def test_details_invalid_user_id():
#     '''Requesting channel details with invalid user id'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)
#     invalid_user_id = 2

#     with pytest.raises(InputError):
#         channel_details_v1(invalid_user_id, channel['channel_id'])
#     with pytest.raises(InputError):
#         channel_details_v1("ThisIsAString", channel['channel_id'])
#     with pytest.raises(InputError):
#         channel_details_v1("1", channel['channel_id'])

# # def test_channel_join_v1():
# #     '''Testings cases for channel_join_v1 with correct parameters'''
# #     clear_v1()
# #     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
# #     channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)
# #     user = auth_register_v1('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')

# #     channel_join_v1(user['auth_user_id'], channel['channel_id'])
# #     channel_list = channels_list_v1(user['auth_user_id'])
# #     assert len(channel_list['channels']) == 1

# # def test_join_invalid_channel_id():
# #     '''Joining a channel with invalid channel id'''
# #     clear_v1()
# #     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
# #     invalid_channel_id = 2

# #     with pytest.raises(InputError):
# #         channel_join_v1(owner['auth_user_id'], invalid_channel_id)
# #     with pytest.raises(InputError):
# #         channel_join_v1(owner['auth_user_id'], "ThisIsAString")
# #     with pytest.raises(InputError):
# #         channel_join_v1(owner['auth_user_id'], '1')

# # def test_join_private_channel():
# #     '''Joining a private channel'''
# #     clear_v1()
# #     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
# #     user = auth_register_v1('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
# #     channel = channels_create_v1(owner['auth_user_id'], 'Channel_Private', False)

# #     with pytest.raises(AccessError):
# #         channel_join_v1(user['auth_user_id'], channel['channel_id'])

# def test_channel_messages_v1():
#     '''Testings cases for channel_messages_v1 with correct parameters'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)
#     message_send_v1(owner['auth_user_id'], channel['channel_id'], 'Hello World')
#     msg = channel_messages_v1(owner['auth_user_id'], channel['channel_id'], 0)
#     assert len(msg['messages']) == 1

# def test_messages_invalid_channel_id():
#     '''Requesting messages from an invalid channel id'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')

#     invalid_channel_id = 2

#     with pytest.raises(InputError):
#         channel_messages_v1(owner['auth_user_id'], invalid_channel_id, 0)
#     with pytest.raises(InputError):
#         channel_messages_v1(owner['auth_user_id'], "ThisIsAString", 0)

# def test_messages_invalid_msg_index():
#     '''Requesting messages from an invalid channel id'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)
#     message_send_v1(owner['auth_user_id'], channel['channel_id'], 'Hello World')
#     msg = channel_messages_v1(owner['auth_user_id'], channel['channel_id'], 0)
#     invalid_msg_index = len(msg['messages'])

#     with pytest.raises(InputError):
#         channel_messages_v1(owner['auth_user_id'], channel['channel_id'], invalid_msg_index)
#     with pytest.raises(InputError):
#         channel_messages_v1(owner['auth_user_id'], channel['channel_id'], -1)

# def test_messages_user_not_member():
#     '''Authorised user is not a member of channel'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     user = auth_register_v1('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
#     channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)

#     with pytest.raises(AccessError):
#         channel_messages_v1(user['auth_user_id'], channel['channel_id'], 0)
#     # with pytest.raises(AccessError):
#     #     channel_messages_v1("NotAValidUID", channel['channel_id'], 0)


# Iteration 2 Tests

# channel_details_v2()
def test_channel_details_v2():
    '''Testings cases for channel_details_v2 with correct parameters'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)

    details = channel_details_v2(owner['token'], channel['channel_id'])
    assert details['name'] == 'Channel_One'
    assert len(details['owner_members']) == 1
    assert len(details['all_members']) == 1

def test_details_invalid_channel_id_v2():
    '''Requesting channel details with invalid channel id'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')

    with pytest.raises(InputError):
        channel_details_v2(owner['token'], 2)
    with pytest.raises(InputError):
        channel_details_v2(owner['token'], "ThisIsAString")
    with pytest.raises(InputError):
        channel_details_v2(owner['token'], '1')

def test_details_invalid_user_id_v2():
    '''Requesting channel details with invalid user id, or user not in channel'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)

    with pytest.raises(AccessError):
        channel_details_v2(9, channel['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v2(user['token'], channel['channel_id'])


# channel_messages_v2()
def test_channel_messages_v2():
    '''Testings cases for channel_messages_v2 with correct parameters'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    message_send_v2(owner['token'], channel['channel_id'], 'Hello World')
    msg = channel_messages_v2(owner['token'], channel['channel_id'], 0)
    assert len(msg['messages']) == 1

def test_messages_invalid_channel_id_v2():
    '''Requesting messages from an invalid channel id'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')

    with pytest.raises(InputError):
        channel_messages_v2(owner['token'], 9, 0)
    with pytest.raises(InputError):
        channel_messages_v2(owner['token'], "ThisIsAString", 0)

def test_messages_invalid_msg_index_v2():
    '''Requesting messages from an invalid channel id'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    message_send_v2(owner['token'], channel['channel_id'], 'Hello World')
    channel_messages_v2(owner['token'], channel['channel_id'], 0)

    with pytest.raises(InputError):
        channel_messages_v2(owner['token'], channel['channel_id'], 111)

def test_messages_user_not_member_v2():
    '''Authorised user is not a member of channel'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)

    with pytest.raises(AccessError):
        channel_messages_v2(user['token'], channel['channel_id'], 0)

# channel_addowner_v1()
def test_channel_addowner_v1():
    '''Tests cases for channel_addowner_v1 where all parameters are valid'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel['channel_id'])
    channel_addowner_v1(owner['token'], channel['channel_id'], user['auth_user_id'])
    details = channel_details_v2(owner['token'], channel['channel_id'])
    assert len(details['owner_members']) == 2

def test_channel_addowner_invalid_channel_id_v1():
    '''Tests cases for channel_addowner_v1 where channel id is invalid'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel['channel_id'])
    with pytest.raises(InputError):
        channel_addowner_v1(owner['token'], channel['channel_id']+1, user['auth_user_id'])

def test_channel_addowner_already_owner_v1():
    '''Tests cases for channel_addowner_v1 where user is already an owner'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    with pytest.raises(InputError):
        channel_addowner_v1(owner['token'], channel['channel_id'], owner['auth_user_id'])

def test_channel_addowner_not_owner_id_v1():
    '''Tests cases for channel_addowner_v1 where auth user is not owner'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel['channel_id'])
    with pytest.raises(AccessError):
        channel_addowner_v1(user['token'], channel['channel_id'], user['auth_user_id'])

def test_channel_addowner_dreams_owner_id_v1():
    '''Tests cases for channel_addowner_v1 where Dreams owner adds an owner'''
    clear_v1()
    dreams_owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    owner = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    user = auth_register_v2('steven.brown@gmail.com', 'pass123', 'Steven', 'Brown')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel['channel_id'])
    channel_addowner_v1(dreams_owner['token'], channel['channel_id'], user['auth_user_id'])

def test_channel_addowner_not_in_channel_v1():
    '''Tests cases for channel_addowner_v1 where user is not in channel'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    with pytest.raises(AccessError):
        channel_addowner_v1(owner['token'], channel['channel_id'], user['auth_user_id'])

# channel_remoevowner_v1()
def test_channel_removeowner_v1():
    '''Tests cases for channel_removeowner_v1 where all parameters are valid'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel['channel_id'])
    channel_addowner_v1(owner['token'], channel['channel_id'], user['auth_user_id'])
    channel_removeowner_v1(owner['token'], channel['channel_id'], user['auth_user_id'])
    details = channel_details_v2(owner['token'], channel['channel_id'])
    assert len(details['owner_members']) == 1

def test_channel_removeowner_invalid_channel_id_v1():
    '''Tests cases for channel_removeowner_v1 where channel id is invalid'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel['channel_id'])
    channel_addowner_v1(owner['token'], channel['channel_id'], user['auth_user_id'])
    with pytest.raises(InputError):
        channel_removeowner_v1(owner['token'], channel['channel_id']+1, user['auth_user_id'])

def test_channel_removeowner_not_owner_v1():
    '''Tests cases for channel_removeowner_v1 where user is not an owner'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel['channel_id'])
    with pytest.raises(InputError):
        channel_removeowner_v1(owner['token'], channel['channel_id'], user['auth_user_id'])

def test_channel_removeowner_no_permission_v1():
    '''Tests cases for channel_removeowner_v1 where auth user has no permission'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel['channel_id'])
    with pytest.raises(AccessError):
        channel_removeowner_v1(user['token'], channel['channel_id'], owner['auth_user_id'])

def test_channel_removeowner_dreams_owner_v1():
    '''Tests cases for channel_removeowner_v1 where Dreams owner adds an owner'''
    clear_v1()
    dreams_owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    owner = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    user = auth_register_v2('steven.brown@gmail.com', 'pass123', 'Steven', 'Brown')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel['channel_id'])
    channel_addowner_v1(owner['token'], channel['channel_id'], user['auth_user_id'])
    channel_removeowner_v1(dreams_owner['token'], channel['channel_id'], user['auth_user_id'])

def test_channel_removeowner_not_in_channel_v1():
    '''Tests cases for channel_removeowner_v1 where user is not in the channel'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    with pytest.raises(InputError):
        channel_removeowner_v1(owner['token'], channel['channel_id'], user['auth_user_id'])

def test_channel_removeowner_only_owner_v1():
    '''Tests cases for channel_removeowner_v1 where all parameters are valid'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    with pytest.raises(InputError):
        channel_removeowner_v1(owner['token'], channel['channel_id'], owner['auth_user_id'])

# channel_leave_v1()
def test_channel_leave_v1():
    '''Tests cases for channel_leave_v1 where all parameters are valid'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel['channel_id'])
    channel_leave_v1(user['token'], channel['channel_id'])
    details = channel_details_v2(owner['token'], channel['channel_id'])
    assert len(details['all_members']) == 1

def test_channel_leave_invalid_channel_id_v1():
    '''Tests cases for channel_leave_v1 where channel id is invalid'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    channel_join_v2(user['token'], channel['channel_id'])
    with pytest.raises(InputError):
        channel_leave_v1(user['token'], channel['channel_id']+1)

def test_channel_leave_not_in_channel_v1():
    '''Tests cases for channel_leave_v1 where user is not in the channel'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v2('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v2(owner['token'], 'Channel_One', True)
    with pytest.raises(AccessError):
        channel_leave_v1(user['token'], channel['channel_id'])

# def test_channel_leave_only_owner_v1():
#     '''Tests cases for channel_leave_v1 where channel id is invalid'''
#     clear_v1()
#     owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     channel = channels_create_v2(owner['token'], 'Channel_One', True)
#     with pytest.raises(InputError):
#         channel_leave_v1(owner['token'], channel['channel_id'])

# test channel_invite channel id InputError
def test_channel_invite_v2_channel_inputError():
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user1 = auth_register_v2('hayden.everest@gmail.com', '123abc', 'Hayden', 'Everest')
    user2 = auth_register_v2('hayden2.everest@gmail.com', '123abc', 'Hayden', 'Everest')
    user3 = auth_register_v2('hayden3.everest@gmail.com', '123abc', 'Hayden', 'Everest')
    invalid_channel_id = 300

    with pytest.raises(InputError):
        channel_invite_v2(owner['token'], invalid_channel_id, user1['auth_user_id'])
    with pytest.raises(InputError):
        channel_invite_v2(owner['token'], "ThisIsAString", user2['auth_user_id'])
    with pytest.raises(InputError):
        channel_invite_v2(owner['token'], '1', user3['auth_user_id'])


# test user id inputError
def test_channel_invite_v2_user_inputError():
    clear_v1()
    user1 = auth_register_v2('john1.smith@gmail.com', 'pass123', 'John', 'Smith')
    user2 = auth_register_v2('hayden4.everest@gmail.com', '123abc', 'Hayden', 'Everest')
    channel = channels_create_v2(user1['token'], 'Channel_One', True)
    invalid_u_id = 200

    with pytest.raises(InputError):
        channel_invite_v2(user1['token'], channel['channel_id'], invalid_u_id)
    with pytest.raises(InputError):
        channel_invite_v2(user2['token'], channel['channel_id'], "ThisIsAString")


# test Access Error (member is already in channel)
def test_channel_invite_v2_accessError():
    clear_v1()
    user4 = auth_register_v2('hayden6.everest@gmail.com', '123abc', 'Hayden', 'Everest')

    with pytest.raises(InputError):
        channel_invite_v2(user4['token'], 1, "1")


# test channel_join channel id InputError
def test_channel_join_v2_channel_inputError():
    clear_v1()
    owner2 = auth_register_v2('john.smith3@gmail.com', 'pass123', 'John', 'Smith')
    owner3 = auth_register_v2('john.smith4@gmail.com', 'pass123', 'John', 'Smith')
    owner4 = auth_register_v2('john.smith5@gmail.com', 'pass123', 'John', 'Smith')
    invalid_channel_id = 400

    with pytest.raises(InputError):
        channel_join_v2(owner2['token'], invalid_channel_id)
    with pytest.raises(InputError):
        channel_join_v2(owner3['token'], "ThisIsAString")
    with pytest.raises(InputError):
        channel_join_v2(owner4['token'], '1')


# test Access Error (member is already in channel)
def test_channel_join_v2_accessError():
    clear_v1()
    owner = auth_register_v2('john.smith6@gmail.com', 'pass123', 'John', 'Smith')
    channel = channels_create_v2(owner['token'], 'Channel_Seven', False)

    with pytest.raises(AccessError):
        channel_join_v2(owner['token'], channel['channel_id'])


# test join
def test_channel_join_v2():
    clear_v1()
    owner11 = auth_register_v2('john.smith12@gmail.com', 'pass123', 'John', 'Smith')
    newchannel = channels_create_v2(owner11['token'], 'Channel_One', True)

    # calculate the number of members in the channel
    len1 = 0
    for channel in data['channels']:
        if channel['channel_id'] == newchannel['channel_id']:
            len1 = len(channel['all_members'])

    # run the channel_join_v1 function
    channel_join_v2(owner11['token'], newchannel['channel_id'])

    # calculate the number of members in the channel
    len2 = 0
    for channel in data['channels']:
        if channel['channel_id'] == newchannel['channel_id']:
            len2 = len(channel['all_members'])

    # join function been called once, so number of members will 1 more than before
    assert (len2 - len1) == 1


# test invite
def test_channel_invite_v2():
    clear_v1()
    # create new member and new channel
    owner = auth_register_v2('john.smith8@gmail.com', 'pass123', 'John', 'Smith')
    newchannel = channels_create_v2(owner['token'], 'Channel_One', True)
    user = auth_register_v2('eliza.jones2@gmail.com', 'pass123', 'Eliza', 'Jones')

    # calculate the number of members in the channel
    len1 = 0
    for channel in data['channels']:
        if channel['channel_id'] == newchannel['channel_id']:
            print('newchannel', newchannel['channel_id'])
            print('channel', channel['channel_id'])
            len1 = len(channel['all_members'])

    # run the channel_invite_v1 function
    channel_invite_v2(owner['token'], newchannel['channel_id'], user['auth_user_id'])

    # calculate the number of members in the channel
    len2 = 0
    for channel in data['channels']:
        if channel['channel_id'] == newchannel['channel_id']:
            len2 = len(channel['all_members'])

    # invite function been called once, so number of members will 1 more than before
    assert (len2 - len1) == 1



# @pytest.fixture
# def channel_setup():
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)

# def test_channel_details_v1():
#     """Testings cases for channel_details_v1 with correct parameters"""
#     clear_v1()
#     owner = auth_register_2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)
#
#     details = channel_details_v2(owner['auth_user_id'], channel['channel_id'])
#     assert details['name'] == 'Channel_One'
#     assert len(details['owner_members']) == 1
#     assert len(details['all_members']) == 1
#
#
# def test_details_invalid_channel_id():
#     '''Requesting channal details with invalid channel id'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#
#     invalid_channel_id = 2
#
#     with pytest.raises(InputError):
#         channel_details_v1(owner['auth_user_id'], invalid_channel_id)
#     with pytest.raises(InputError):
#         channel_details_v1(owner['auth_user_id'], "ThisIsAString")
#     with pytest.raises(InputError):
#         channel_details_v1(owner['auth_user_id'], '1')
#
#
# def test_details_invalid_user_id():
#     '''Requesting channal details with invalid user id'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)
#     invalid_user_id = 2
#
#     with pytest.raises(InputError):
#         channel_details_v1(invalid_user_id, channel['channel_id'])
#     with pytest.raises(InputError):
#         channel_details_v1("ThisIsAString", channel['channel_id'])
#     with pytest.raises(InputError):
#         channel_details_v1("1", channel['channel_id'])
#

# def test_channel_join_v1():
#     '''Testings cases for channel_join_v1 with correct parameters'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)
#     user = auth_register_v1('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')

#     channel_join_v1(user['auth_user_id'], channel['channel_id'])
#     channel_list = channels_list_v1(user['auth_user_id'])
#     assert len(channel_list['channels']) == 1

# def test_join_invalid_channel_id():
#     '''Joining a channel with invalid channel id'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     invalid_channel_id = 2

#     with pytest.raises(InputError):
#         channel_join_v1(owner['auth_user_id'], invalid_channel_id)
#     with pytest.raises(InputError):
#         channel_join_v1(owner['auth_user_id'], "ThisIsAString")
#     with pytest.raises(InputError):
#         channel_join_v1(owner['auth_user_id'], '1')

# def test_join_private_channel():
#     '''Joining a private channel'''
#     clear_v1()
#     owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
#     user = auth_register_v1('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
#     channel = channels_create_v1(owner['auth_user_id'], 'Channel_Private', False)

#     with pytest.raises(AccessError):
#         channel_join_v1(user['auth_user_id'], channel['channel_id'])
"""
def test_channel_messages_v1():
    '''Testings cases for channel_messages_v1 with correct parameters'''
    clear_v1()
    owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)
    message_send_v1(owner['auth_user_id'], channel['channel_id'], 'Hello World')
    msg = channel_messages_v1(owner['auth_user_id'], channel['channel_id'], 0)
    assert len(msg['messages']) == 1

def test_messages_invalid_channel_id():
    '''Requesting messages from an invalid channel id'''
    clear_v1()
    owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')

    invalid_channel_id = 2

    with pytest.raises(InputError):
        channel_messages_v1(owner['auth_user_id'], invalid_channel_id, 0)
    with pytest.raises(InputError):
        channel_messages_v1(owner['auth_user_id'], "ThisIsAString", 0)

def test_messages_invalid_msg_index():
    '''Requesting messages from an invalid channel id'''
    clear_v1()
    owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)
    message_send_v1(owner['auth_user_id'], channel['channel_id'], 'Hello World')
    msg = channel_messages_v1(owner['auth_user_id'], channel['channel_id'], 0)
    invalid_msg_index = len(msg['messages'])

    with pytest.raises(InputError):
        channel_messages_v1(owner['auth_user_id'], channel['channel_id'], invalid_msg_index)
    with pytest.raises(InputError):
        channel_messages_v1(owner['auth_user_id'], channel['channel_id'], -1)

def test_messages_user_not_member():
    '''Authorised user is not a member of channel'''
    clear_v1()
    owner = auth_register_v1('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    user = auth_register_v1('eliza.jones@gmail.com', 'pass123', 'Eliza', 'Jones')
    channel = channels_create_v1(owner['auth_user_id'], 'Channel_One', True)

    with pytest.raises(AccessError):
        channel_messages_v1(user['auth_user_id'], channel['channel_id'], 0)
    # with pytest.raises(AccessError):
    #     channel_messages_v1("NotAValidUID", channel['channel_id'], 0) 
"""
