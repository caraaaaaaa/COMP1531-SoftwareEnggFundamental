import pytest

from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.channel import channel_invite_v2, channel_details_v2, channel_messages_v2
from src.notifications import notifications_get_v1
from src.dm import dm_create_v1, handle_finder, dm_invite_v1, dm_details_v1
from src.message import message_senddm_v1, message_send_v2, message_share_v1, message_react_v1
from src.standup import standup_start_v1, standup_send_v1
from src.other import clear_v1
from time import sleep
from src.error import InputError, AccessError

'''Tests for notifications get functions'''

def test_notifications_get_dm():
    '''Test basic functionality for notifications in dms'''
    clear_v1()
    
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    member2 = auth_register_v2('jake.smith@gmail.com', 'pass123', 'Jake', 'Smith')
    dm = dm_create_v1(owner['token'], [member1['auth_user_id']])
    memberHandle = handle_finder(member1['auth_user_id'])
    ownerHandle = handle_finder(owner['auth_user_id'])
    msgString = f"check this @{memberHandle} guy out"
    message_senddm_v1(owner['token'], dm['dm_id'], msgString)
    dm_invite_v1(owner['token'], dm['dm_id'], member2['auth_user_id'])
    
    notif = notifications_get_v1(member1['token'])
    
    assert len(notif['notifications']) == 2
    
    assert notif['notifications'][0]['channel_id'] == -1
    assert notif['notifications'][0]['dm_id'] == dm['dm_id']
    assert notif['notifications'][0]['notification_message'] == f"{ownerHandle} tagged you in {dm['dm_name']}: {msgString[0:20]}"
    
    assert notif['notifications'][1]['channel_id'] == -1
    assert notif['notifications'][1]['dm_id'] == dm['dm_id']
    assert notif['notifications'][1]['notification_message'] == f"{ownerHandle} added you to {dm['dm_name']}"

    
    notif = notifications_get_v1(member2['token'])
    
    assert len(notif['notifications']) == 1
    
    assert notif['notifications'][0]['channel_id'] == -1
    assert notif['notifications'][0]['dm_id'] == dm['dm_id']
    assert notif['notifications'][0]['notification_message'] == f"{ownerHandle} added you to {dm['dm_name']}"
    
def test_notification_get_channels():
    '''Test basic functionality of notifications from channels'''

    clear_v1()
    
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    channel = channels_create_v2(owner['token'], 'My Channel', True)
    channel_invite_v2(owner['token'], channel['channel_id'], member1['auth_user_id'])
    memberHandle = handle_finder(member1['auth_user_id'])
    ownerHandle = handle_finder(owner['auth_user_id'])
    msgString = f"check this @{memberHandle} guy out"
    message_send_v2(owner['token'], channel['channel_id'], msgString)
    channel_details = channel_details_v2(owner['token'], channel['channel_id'])
    
    
    notif = notifications_get_v1(member1['token'])
    assert len(notif['notifications']) == 2
    
    assert notif['notifications'][0]['channel_id'] == channel['channel_id']
    assert notif['notifications'][0]['dm_id'] == -1
    assert notif['notifications'][0]['notification_message'] == f"{ownerHandle} tagged you in {channel_details['name']}: {msgString[0:20]}"
    
    assert notif['notifications'][1]['channel_id'] == channel['channel_id']
    assert notif['notifications'][1]['dm_id'] == -1
    assert notif['notifications'][1]['notification_message'] == f"{ownerHandle} added you to {channel_details['name']}"

def test_notifications_get_message_shared():
    '''Test if notification is raised when a message is shared'''
    clear_v1()
    
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    dm1 = dm_create_v1(owner['token'], [])
    dm2 = dm_create_v1(owner['token'], [])
    ownerHandle = handle_finder(owner['auth_user_id'])
    msgString = f'hey, @{ownerHandle}' 
    message = message_senddm_v1(owner['token'], dm1['dm_id'], msgString)
    message_share_v1(owner['token'], message, '', -1, dm2['dm_id'])
    notif = notifications_get_v1(owner['token'])
    assert len(notif['notifications']) == 2
    assert notif['notifications'][0]['dm_id'] == dm2['dm_id']
    assert notif['notifications'][0]['channel_id'] == -1
    assert notif['notifications'][0]['notification_message'] == f'{ownerHandle} tagged you in {dm2["dm_name"]}: ' + f'"{msgString[0:20]}"'
    
def test_notifications_more_messages():
    '''Test whether the 20 most recent notifications are sent'''
    
    clear_v1()
    
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    channel = channels_create_v2(owner['token'], 'My Channel', True)
    channel_invite_v2(owner['token'], channel['channel_id'], member1['auth_user_id'])
    memberHandle = handle_finder(member1['auth_user_id'])
    ownerHandle = handle_finder(owner['auth_user_id'])
    msgString = f"@{memberHandle} this guy"
    counter = 0
    while counter < 19:
        message_send_v2(owner['token'], channel['channel_id'], msgString)
        counter += 1
    channel_details = channel_details_v2(owner['token'], channel['channel_id'])
    
    notif = notifications_get_v1(member1['token'])
    assert len(notif['notifications']) == 20
    assert notif['notifications'][19]['notification_message'] == f"{ownerHandle} added you to {channel_details['name']}"
    
    '''Test if the 20 most recent messages are shown in notifications'''
    message_send_v2(owner['token'], channel['channel_id'], msgString)
    notif = notifications_get_v1(member1['token'])        
    assert len(notif['notifications']) == 20
    assert notif['notifications'][19]['notification_message'] == f'{ownerHandle} tagged you in {channel_details["name"]}: {msgString[0:20]}'


def test_notifications_invalid_token():
    '''Test when token doesn't exist'''
    clear_v1()
    
    auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    
    with pytest.raises(AccessError):
        notifications_get_v1(0)
    with pytest.raises(AccessError):
        notifications_get_v1({})

def test_notification_no_notifs():
    '''Test when there are no notifications'''
    
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    notif = notifications_get_v1(owner['token'])
    
    assert len(notif['notifications']) == 0


def test_notifications_multiple_tags():
    '''Test for multiple tags'''

    clear_v1()
    
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    channel = channels_create_v2(owner['token'], 'My Channel 1', True)
    channel_invite_v2(owner['token'], channel['channel_id'], member1['auth_user_id'])
    
    memberHandle = handle_finder(member1['auth_user_id'])
    ownerHandle = handle_finder(owner['auth_user_id'])
    msgString = f"check this @{memberHandle} @{ownerHandle} guy out"
    message_send_v2(owner['token'], channel['channel_id'], msgString)
    channel_details = channel_details_v2(owner['token'], channel['channel_id'])
    notif = notifications_get_v1(member1['token'])
    
    assert notif['notifications'][0]['channel_id'] == channel['channel_id']
    assert notif['notifications'][0]['dm_id'] == -1
    assert notif['notifications'][0]['notification_message'] == f"{ownerHandle} tagged you in {channel_details['name']}: {msgString[0:20]}"
    
    notif = notifications_get_v1(owner['token'])
    
    assert notif['notifications'][0]['channel_id'] == channel['channel_id']
    assert notif['notifications'][0]['dm_id'] == -1
    assert notif['notifications'][0]['notification_message'] == f"{ownerHandle} tagged you in {channel_details['name']}: {msgString[0:20]}"

def test_notifications_untriggered_tag():
    '''Test for untriggered tags'''
    clear_v1()
    
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    member2 = auth_register_v2('jake.smith@gmail.com', 'pass123', 'Jake', 'Smith')
    dm = dm_create_v1(owner['token'], [member1['auth_user_id']])
    member2Handle = handle_finder(member2['auth_user_id'])
    msgString = f"check this @{member2Handle} guy out"
    message_senddm_v1(owner['token'], dm['dm_id'], msgString)
    
    notif = notifications_get_v1(member2['token'])
    
    assert len(notif['notifications']) == 0
    
    channel = channels_create_v2(owner['token'], 'My Channel 1', True)
    message_send_v2(owner['token'], channel['channel_id'], msgString)
    
    notif = notifications_get_v1(member2['token'])
    
    assert len(notif['notifications']) == 0

def test_notifications_message_react():
    '''Test for notifications when someone reacts to a users message'''
    clear_v1()
    
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    owner_handle = handle_finder(owner['auth_user_id'])
    dm = dm_create_v1(owner['token'], [])
    channel = channels_create_v2(owner['token'], 'Channel1', True)
    message1 = message_senddm_v1(owner['token'], dm['dm_id'], 'hello')
    message2 = message_send_v2(owner['token'], channel['channel_id'], 'is that you?')
    message_react_v1(owner['token'], message1, 1)
    message_react_v1(owner['token'], message2, 1)
    details = channel_details_v2(owner['token'], channel['channel_id'])
    notif = notifications_get_v1(owner['token'])
    assert len(notif['notifications']) == 2
    assert notif['notifications'] == [{
        'channel_id': channel['channel_id'],
        'dm_id': -1,
        'notification_message': f"{owner_handle} reacted to your message in {details['name']}",
    },
    {
        'channel_id': -1,
        'dm_id': dm['dm_id'],
        'notification_message': f"{owner_handle} reacted to your message in {dm['dm_name']}",
    }]

def test_notifications_standup():
    '''Test for notifications when message is sent from standup'''
    clear_v1()
    
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    owner_handle = handle_finder(owner['auth_user_id'])
    channel = channels_create_v2(owner['token'], 'Channel1', True)
    standup_start_v1(owner['token'], channel['channel_id'], 5)
    standup_send_v1(owner['token'], channel['channel_id'], f'@{owner_handle} hello')
    details = channel_details_v2(owner['token'], channel['channel_id'])
    sleep(5)
    message = channel_messages_v2(owner['token'], channel['channel_id'], 0)['messages'][0]['message']
    notif = notifications_get_v1(owner['token'])
    assert len(notif['notifications']) == 1
    assert notif['notifications'][0] == {
        'channel_id': channel['channel_id'],
        'dm_id': -1,
        'notification_message': f"{owner_handle} tagged you in {details['name']}: {message[0:20]}",
    }
    
    
