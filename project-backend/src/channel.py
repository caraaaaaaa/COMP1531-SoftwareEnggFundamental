"""Functions relating to channel"""
from src.data import data
from src.error import InputError, AccessError
from src.notifications import add_notification_invited
from src.dm import handle_finder
import datetime
import time


def channel_invite_v2(token, channel_id, u_id):
    '''
    Invites a user (with user id u_id) to join a channel with ID channel_id. 
    Once invited the user is added to the channel immediately
    Arguments:
        token (string)           - identifier unique to each user
        channel_id (integer)     - identifier unique to each channel
        u_id (integer)           - identifier unique to each user
    Exceptions:
        InputError             - channel_id does not refer to a valid channel.
                               - u_id does not refer to a valid user
        AccessError            - the authorised user is not already a member of the channel

    Return values:
         {}
    '''
    uid_error = 0
    uid_exist_error = 0
    for us in data['users']:
        if us['u_id'] == u_id:
            uid_error = 1
    # raise Input error or access error
    channel_error = 0

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel_error = 1
            # find user with token
            for auth in channel['all_members']:
                if auth['u_id'] == u_id:
                    uid_exist_error = 1
    if channel_error == 0:
        raise InputError
    if uid_error == 0:
        raise InputError
    if uid_exist_error == 1:
        raise AccessError

    #Add notification when invited to channel
    add_notification_invited(token, u_id, channel_id, 'channel')

    password = ''
    email = ''
    first = ''
    last = ''
    handle = ''
    # find user's detail
    for user in data['users']:
        if user['u_id'] == u_id:
            password = user['password']
            first = user['name_first']
            last = user['name_last']
            email = user['email']
            handle = user['handle_str']
            token = user['token']
            user['channels_num'] += 1

            user['channel_time'] = int(time.time())



    # create a dictionary to store information of new member
    new = {
        'u_id': u_id,
        'password': password,
        'email': email,
        'name_first': first,
        'name_last': last,
        'handle_str': handle,
        'token': token
    }

    # find the channel and append new member's information in it
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(new)

    return {
    }


def channel_join_v2(token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join, 
    adds them to that channel
    Arguments:
        token (string)           - identifier unique to each user
        channel_id (integer)     - identifier unique to each channel
    Exceptions:
        InputError             - channel_id does not refer to a valid channel.
        AccessError            - channel_id refers to a channel that is private

    Return values:
         {}
    '''
    channel_error = 0
    access_error = 0
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel_error = 1
            if not channel['is_public']:
                access_error = 1
    if channel_error == 0:
        raise InputError
    if access_error == 1:
        raise AccessError

    u_id = 0
    password = ''
    email = ''
    first = ''
    last = ''
    handle = ''
    # find user's first name and last name
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            password = user['password']
            first = user['name_first']
            last = user['name_last']
            email = user['email']
            handle = user['handle_str']
            token = user['token']
            user['channels_num'] += 1
            user['channel_time'] = int(time.time())

    # create a dictionary to store information of new member
    new = {}
    new['u_id'] = u_id
    new['password'] = password
    new['email'] = email
    new['name_first'] = first
    new['name_last'] = last
    new['handle_str'] = handle
    new['token'] = token

    # find the channel and append new member's information in it
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(new)

    return {
    }

def channel_details_v2(token, channel_id):
    '''Function that returns the details given channel_id and auth_user_id '''
    # Error Trapping

    if is_valid_channel(channel_id) is False:
        # Invalid channel_id
        raise InputError
    user = user_finder(token)
    if user is None:
        # Invalid auth_user_id
        raise AccessError
    if is_user_in_channel(user['u_id'], channel_id) is False:
        # User is not a memeber of the channel
        raise AccessError

    channel = channel_finder(channel_id)

    channel_details = {
        'name' : channel['name'],
        'owner_members': [
            # Loops through each owner in the channel and adds to array
            {
                'u_id': owner['u_id'],
                'name_first': owner['name_first'],
                'name_last': owner['name_last'],
            }
            for owner in channel['owner_members']
        ],
        'all_members': [
            # Loops through each member in the channel and adds to array
            {
                'u_id': member['u_id'],
                'name_first': member['name_first'],
                'name_last': member['name_last'],
            }
            for member in channel['all_members']
        ],
    }
    return channel_details

def channel_messages_v2(token, channel_id, start):
    '''Function that returns up to 50 messsages from a given server, must be
        requested by a user within the server '''
    end = start + 50

    # Error Trapping
    channel = channel_finder(channel_id)
    if channel is None:
        # Invalid channel_id
        raise InputError
    user = user_finder(token)
    if user is None:
        # Invalid token
        raise AccessError
    if is_user_in_channel(user['u_id'], channel_id) is False:
        # User is not a memeber of the channel
        raise AccessError

    if start < 0:
        # invalid msg index
        raise InputError
    total_num_msg = len(channel['messages'])
    if total_num_msg < end:
        end = -1
    if total_num_msg < start:
        # start is greater than the total number of messages in the channel
        raise InputError

    channel = channel_finder(channel_id)

    channel_messages = {
        'messages' : [
            {
                'message_id': message['message_id'],
                'u_id' : message['u_id'],
                'message' : message['message'],
                'time_created' : message['time_created'],
                'reacts': message['reacts'],
                'is_pinned': message['is_pinned']
            }
            for message in channel['messages']

        ],
        'start' : start,
        'end' : end
    }

    return channel_messages

def channel_leave_v1(token, channel_id):
    is_user_in_channel = 0
    is_user_owner = 0
    channel = channel_finder(channel_id)
    if channel is None:
        # Invalid channel_id
        raise InputError
    user = user_finder(token)
    u_id = user['u_id']
    if user is None:
        # Invalid token
        raise AccessError
    for member in channel['all_members']:
        if member['u_id'] == user['u_id']:
            is_user_in_channel = 1
            break
    if is_user_in_channel != 1:
        raise AccessError
    for owner in channel['owner_members']:
        if owner['u_id'] == user['u_id']:
            is_user_owner = 1
            break

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for removed_user in channel['all_members']:
                if removed_user['u_id'] == u_id:
                    channel['all_members'].remove(removed_user)
            if is_user_owner == 1:
                for removed_user in channel['owner_members']:
                    if removed_user['u_id'] == u_id:
                        channel['all_members'].remove(removed_user)

    for user in data['users']:
        if user['token'] == token:
            user['channels_num'] -= 1
            user['channel_time'] = int(time.time())

    return {
    }


def channel_addowner_v1(token, channel_id, u_id):
    # Error trapping
    is_auth_user_owner = 0
    is_user_in_channel = 0
    channel = channel_finder(channel_id)
    if channel is None:
        # Invalid channel_id
        raise InputError
    auth_user = user_finder(token)
    auth_uid = auth_user['u_id']
    if auth_user is None:
        # Invalid token
        raise AccessError
    user = user_finder(token)
    if user is None:
        # Invalid token
        raise AccessError
    # Check if user is already owner
    for owner in channel['owner_members']:
        if owner['u_id'] == u_id:
            raise InputError
    # Checks if auth_user is owner
    for owner in channel['owner_members']:
        if owner['u_id'] == auth_uid:
            is_auth_user_owner = 1
            break
    # Checks if auth_user is Dreams Owner
    if auth_user['permission_id'] == 1:
        is_auth_user_owner = 1
    if is_auth_user_owner != 1:
        raise AccessError
    # Checks if user is in channel
    for member in channel['all_members']:
        if member['u_id'] == u_id:
            is_user_in_channel = 1
            break
    if is_user_in_channel != 1:
        raise AccessError

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for new_owner in channel['all_members']:
                if new_owner['u_id'] == u_id:
                    channel['owner_members'].append(new_owner)
                    break


    return {
    }

def channel_removeowner_v1(token, channel_id, u_id):
    # Error trapping
    is_auth_user_owner = 0
    is_user_in_channel = 0
    is_user_owner = 0
    channel = channel_finder(channel_id)
    if channel is None:
        # Invalid channel_id
        raise InputError
    auth_user = user_finder(token)
    auth_uid = auth_user['u_id']
    if auth_user is None:
        # Invalid token
        raise AccessError
    user = user_finder(token)
    if user is None:
        # Invalid token
        raise AccessError
    # Check if user is already owner
    for owner in channel['owner_members']:
        if owner['u_id'] == u_id:
            is_user_owner = 1
            break
    if is_user_owner == 0:
        raise InputError
    # Checks if auth_user is owner
    for owner in channel['owner_members']:
        if owner['u_id'] == auth_uid:
            is_auth_user_owner = 1
            break
    # Checks if auth_user is Dreams Owner
    if auth_user['permission_id'] == 1:
        is_auth_user_owner = 1
    if is_auth_user_owner != 1:
        raise AccessError
    # Checks if user is in channel
    for member in channel['all_members']:
        if member['u_id'] == u_id:
            is_user_in_channel = 1
            break
    if is_user_in_channel != 1:
        raise AccessError
    if len(channel['owner_members']) == 1:
        raise InputError

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for new_owner in channel['all_members']:
                if new_owner['u_id'] == u_id:
                    channel['owner_members'].remove(new_owner)
                    break

    return {
    }

def is_valid_channel(channel_id):
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return True
        else:
            return False
    return False

def user_finder(token):
    for user in data['users']:
        if token == user['token']:
            return user

def channel_finder(channel_id):
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return channel

def is_user_in_channel(u_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for members in channel['all_members']:
                if u_id == members['u_id']:
                    return True
    return False

