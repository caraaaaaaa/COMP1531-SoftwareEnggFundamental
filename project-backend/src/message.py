'''functions relating to messages'''
from src.data import data
from datetime import datetime
from src.error import InputError, AccessError
from src.notifications import add_notification_tagged, add_notification_react
from threading import Timer


def message_send_v2(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id.
    Note: Each message should have it's own unique ID. I.E. No messages should
    share an ID with another message, even if that other message is in a
    different channel.
    Arguments:
        token (string)      - identifier unique to each user
        channel_id (integer)- identifier unique to each channel
        message (string)    - a string containing the message to be sent

    Exceptions:
        InputError      - Message is more than 1000 characters
        AccessError     - when the authorised user has not joined the channel
                            they are trying to post to
    Return Values:
        Return { message_id } on successful operation
    '''
    if len(message) > 1000:
        raise InputError
    user = user_finder(token)
    if user == None:
        raise AccessError

    data['message_id'] += 1
    data['channels'][channel_id - 1]['messages'].append({
        'message_id': data['message_id'],
        'u_id': user['u_id'],
        'message': message,
        'time_created': int(datetime.timestamp(datetime.now())),
        'reacts' : [],
        'is_pinned': False,
    })

    add_notification_tagged(token, message, channel_id, 'channel')

    return data['message_id']

def message_remove_v1(token, message_id):
    '''
    Given a message_id for a message, this message is removed
    from the channel/DM
    Arguments:
        token (string)      - identifier unique to each user
        message_id (integer)- identifier unique to each message

    Exceptions:
        InputError      - Message (based on ID) no longer exists
        AccessError     - Message with message_id was sent by the authorised
                            user making this request
                        - The authorised user is an owner of this channel
                            (if it was sent to a channel) or the **Dreams**

    Return Values:
        Return {} on successful operation
    '''
    user = user_finder(token)
    if user == None:
        raise AccessError
    message_found = False
    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                #found the message check if user is eligble
                message_found = True
                if user['u_id'] != message['u_id']:
                    owner = False
                    for member in channel["owner_members"]:
                        if member['u_id'] == user['u_id']:
                            owner = True
                    if owner == False:
                        raise AccessError
                else:
                    #user is eligble, delete message
                    data['channels'][channel['channel_id'] -1]['messages'].remove(message)

        if message_found == False:
            #message is deleted
            raise InputError
    return {}

def message_edit_v2(token, message_id, message):
    '''
    Given a message, update its text with new text. If the new message is an
    empty string, the message is deleted.
    Arguments:
        token (string)      - identifier unique to each user
        message_id (integer)- identifier unique to each message
        message (string)    - a string containing the message to be sent

    Exceptions:
        InputError      - Length of message is over 1000 characters
                        - Message_id refers to a deleted message
        AccessError     - Message with message_id was sent by the authorised
                            user making this request
                        - The authorised user is an owner of this channel
                            (if it was sent to a channel) or the **Dreams**

    Return Values:
        Return {} on successful operation
    '''
    if len(message) > 1000:
        raise InputError
    user = user_finder(token)
    if user == None:
        raise AccessError
    if message == '':
        return message_remove_v1(token, message_id)
    message_found = False
    for channel in data['channels']:
        for channel_message in channel['messages']:
            if channel_message['message_id'] == message_id:
                #found the message check if user is eligble
                message_found = True
                if user['u_id'] != channel_message['u_id']:
                    owner = False
                    for member in channel["owner_members"]:
                        if member['u_id'] == user['u_id']:
                            owner = True
                    if owner == False:
                        raise AccessError
                else:
                    #user is eligble, edit message
                    #data['channels'][channel['channel_id'] -1]['messages'] = message
                    channel_message['message'] = message
        if message_found == False:
            #message is deleted
            raise InputError
    return {}

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    '''
    Given a message_id send corresponding message to another channel/dm
    Arguments:
        token (string)           - identifier unique to each user
        og_message_id (integer)  - identifier unique to each message
        message (string)         - a string containing the message to be sent
        channel_id (integer)     - identifier unique to each channel
        dm_id (integer)          - identifier unique to each dm

    Exceptions:
        AccessError     - the authorised user has not joined the channel or
                            DM they are trying to share the message to

    Return Values:
        Return {shared_message_id} on successful operation
    '''
    user = user_finder(token)
    if user == None:
        raise AccessError
    user_found = False
    if dm_id == -1:
        for channel in data['channels']:
            if channel['channel_id'] == channel_id:
                for member in channel["all_members"]:
                    if member['u_id'] == user['u_id']:
                        user_found = True
    else:
        for dm in data['dms']:
            if dm['dm_id'] == dm_id:
                for member in dm["members"]:
                    if member['u_id'] == user['u_id']:
                        user_found = True
    if user_found == False:
        raise AccessError

    for channel in data['channels']:
        for channel_message in channel['messages']:
            if channel_message['message_id'] == og_message_id:
                og_message = channel_message['message']

    for dm in data['dms']:
        for dm_message in dm['messages']:
            if dm_message['message_id'] == og_message_id:
                og_message = dm_message['message']

    #found the message
    if message == '':
        shared_message = '"' + og_message + '"'
        print(shared_message)
        print(isinstance(shared_message, str))
    else:
        shared_message = '"' + og_message + '"\n' + message

    if dm_id == -1:
        data['message_id'] += 1
        data['channels'][channel_id - 1]['messages'].append({
            'message_id': data['message_id'],
            'u_id': user['u_id'],
            'message': shared_message,
            'time_created': int(datetime.timestamp(datetime.now())),
            'reacts' : [],
            'is_pinned' : False,
        })

        add_notification_tagged(token, shared_message, channel_id, 'channel')

        return data['message_id']
    else:
        data['message_id'] += 1
        data['dms'][dm_id - 1]['messages'].append({
            'message_id': data['message_id'],
            'u_id': user['u_id'],
            'message': shared_message,
            'time_created': int(datetime.timestamp(datetime.now())),
            'reacts' : [],
            'is_pinned' : False,
        })
        add_notification_tagged(token, shared_message, dm_id, 'dm')

        return data['message_id']






def message_senddm_v1(token, dm_id, message):
    '''
    Send a message from authorised_user to the DM specified by dm_id.
    Arguments:
        token (string)      - identifier unique to each user
        dm_id (integer)     - identifier unique to each dm
        message (string)    - a string containing the message to be sent

    Exceptions:
        InputError      - Length of message is over 1000 characters
        AccessError     - when the authorised user is not a member of the
                            DM they are trying to post to

    Return Values:
        Return { message_id } on successful operation
    '''
    if len(message) > 1000:
        raise InputError
    user = user_finder(token)
    if user == None:
        raise AccessError
    user_found = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            for member in dm["members"]:
                if member['u_id'] == user['u_id']:
                    user_found = True
    if user_found == False:
        raise AccessError
    data['message_id'] += 1
    data['dms'][dm_id - 1]['messages'].insert(0, {
        'message_id': data['message_id'],
        'u_id': user['u_id'],
        'message': message,
        'time_created': int(datetime.timestamp(datetime.now())),
        'reacts' : [],
        'is_pinned' : False,
    })
    add_notification_tagged(token, message, dm_id, 'dm')
    return data['message_id']

def user_finder(token):
    for user in data['users']:
        if token == user['token']:
            return user

def message_sendlater_v1(token, channel_id, message, time_sent):
    '''
    Send a message from authorised_user to the channel specified by channel_id
    automatically at a specified time in the future
    Arguments:
        token (string)           - identifier unique to each user
        channel_id (integer)     - identifier unique to each channel
        message (string)         - a string containing the message to be sent
        time_sent (datetime)     - time on which the message will be sent

    Exceptions:
        InputError      - Length of message is over 1000 characters
                        - Channel ID is not a valid channel
                        - Time sent is a time in the past
        AccessError     - when the authorised user is not a member of the
                            channel they are trying to post to

    Return Values:
        Return {} on successful operation
    '''
    if len(message) > 1000:
        raise InputError
    user = user_finder(token)
    if user == None:
        raise AccessError
    if channel_id > len(data['channels'] or channel_id <= 0):
        raise InputError
    user_found = False
    for member in data['channels'][channel_id - 1]['all_members']:
        if member['u_id'] == user['u_id']:
            user_found = True
    if user_found == False:
        raise AccessError
    time_left = time_sent - datetime.timestamp(datetime.now())
    if time_left < 0:
        raise InputError

    data['message_id'] += 1
    t = Timer(time_left, message_send_v2, args = [token, channel_id, message])
    t.start()

    add_notification_tagged(token, message, channel_id, 'channel')

    return data['message_id']


def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    '''
    Send a message from authorised_user to the DM specified by
    dm_id automatically at a specified time in the future
    Arguments:
        token (string)           - identifier unique to each user
        dm_id (integer)          - identifier unique to each dm
        message (string)         - a string containing the message to be sent
        time_sent (datetime)     - time on which the message will be sent

    Exceptions:
        InputError      - Length of message is over 1000 characters
                        - dm ID is not a valid dm
                        - Time sent is a time in the past
        AccessError     - when the authorised user is not a member of the
                            DM they are trying to post to

    Return Values:
        Return {} on successful operation
    '''
    if len(message) > 1000:
        raise InputError
    user = user_finder(token)
    if user == None:
        raise AccessError
    if dm_id > len(data['dms'] or dm_id <= 0):
        raise InputError
    user_found = False
    for member in data['dms'][dm_id - 1]['members']:
        if member['u_id'] == user['u_id']:
            user_found = True
    if user_found == False:
        raise AccessError
    time_left = time_sent - datetime.timestamp(datetime.now())
    if time_left < 0:
        raise InputError

    data['message_id'] += 1
    t = Timer(time_left, message_senddm_v1, args = [token, dm_id, message])
    t.start()

    add_notification_tagged(token, message, dm_id, 'channel')

    return data['message_id']

def message_react_v1(token, message_id, react_id):
    '''
    Given a message within a channel or DM the authorised user is part of,
    add a "react" to that particular message
    Arguments:
        token (string)           - identifier unique to each user
        message_id (integer)     - identifier unique to each message
        react_id (integer)       - identifier unique to each react

    Exceptions:
        InputError      - message_id is not a valid message within a channel or
                            DM that the authorised user has joined
                        - react_id is not a valid React ID. The only valid react
                            ID the frontend has is 1l
                        - Message with ID message_id already contains an active
                            React with ID react_id from the authorised user
        AccessError     - The authorised user is not a member of the channel
                            or DM that the message is within

    Return Values:
        Return {} on successful operation
    '''
    user = user_finder(token)
    if user == None:
        raise AccessError
    if react_id != 1:
        raise InputError
    msg_found = False
    user_found = False
    is_channel = False
    msg_idx = 0
    for channel in data['channels']:
        for channel_message in channel['messages']:
            if channel_message['message_id'] == message_id:
                target_channel = channel['channel_id']
                msg_idx = channel['messages'].index(channel_message)
                msg_found = True
                is_channel = True
                for member in channel['all_members']:
                    if member['u_id'] == user['u_id']:
                        user_found = True

    for dm in data['dms']:
        for dm_message in dm['messages']:
            if dm_message['message_id'] == message_id:
                target_dm = dm['dm_id']
                msg_idx = dm['messages'].index(dm_message)
                msg_found = True
                for member in dm['members']:
                    if member['u_id'] == user['u_id']:
                        user_found = True
    if msg_found == False:
        raise InputError
    if user_found == False:
        raise AccessError

    if is_channel == True:
        for react in data['channels'][target_channel - 1]['messages'][msg_idx]['reacts']:
            if react['react_id'] == react_id:
                #react exits
                if user['u_id'] in react['u_ids']:
                    raise InputError
                react['u_ids'].append(user['u_id'])
                return {}
        data['channels'][target_channel - 1]['messages'][msg_idx]['reacts'].append({
            'u_ids': [user['u_id']],
            'react_id' : react_id
        })
        add_notification_react(token, message_id, target_channel, 'channel')
    else:
        for react in data['dms'][target_dm - 1]['messages'][msg_idx]['reacts']:
            if react['react_id'] == react_id:
                #react exits
                if user['u_id'] in react['u_ids']:
                    raise InputError
                react['u_ids'].append(user['u_id'])
                return {}
        data['dms'][target_dm - 1]['messages'][msg_idx]['reacts'].append({
            'u_ids': [user['u_id']],
            'react_id' : react_id
        })
        add_notification_react(token, message_id, target_dm, 'dm')
    return {}

def message_unreact_v1(token, message_id, react_id):
    '''
    Given a message within a channel or DM the authorised user is part of,
    remove a "react" to that particular message
    Arguments:
        token (string)           - identifier unique to each user
        message_id (integer)     - identifier unique to each message
        react_id (integer)       - identifier unique to each react

    Exceptions:
        InputError      - message_id is not a valid message within a channel or
                            DM that the authorised user has joined
                        - react_id is not a valid React ID. The only valid react
                            ID the frontend has is 1l
                        - Message with ID message_id does not contain an active
                            React with ID react_id from the authorised user
        AccessError     - The authorised user is not a member of the channel
                            or DM that the message is within

    Return Values:
        Return {} on successful operation
    '''
    u_id = 0
    is_channel = False
    # is_dm = False
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
    if u_id == 0:
        raise AccessError
    if react_id != 1:
        raise InputError
    msg_found = False
    user_found = False
    msg_idx = 0
    for channel in data['channels']:
        for channel_message in channel['messages']:
            if channel_message['message_id'] == message_id:
                msg_idx = channel['messages'].index(channel_message)
                target_channel = channel['channel_id']
                msg_found = True
                is_channel = True
                for member in channel['all_members']:
                    if member['u_id'] == user['u_id']:
                        user_found = True
    if msg_found == False:
        for dm in data['dms']:
            for dm_message in dm['messages']:
                if dm_message['message_id'] == message_id:
                    msg_idx = dm['messages'].index(dm_message)
                    target_dm = dm['dm_id']
                    msg_found = True
                    for member in dm['members']:
                        if member['u_id'] == user['u_id']:
                            user_found = True
    if msg_found == False:
        raise InputError
    if user_found == False:
        raise AccessError

    if is_channel == True:
        for react in data['channels'][target_channel - 1]['messages'][msg_idx]['reacts']:
            if react['react_id'] == react_id:
                #react exits
                if user['u_id'] in react['u_ids']:
                    react['u_ids'].remove(user['u_id'])
                    print(react['u_ids'])
                    if len(react['u_ids']) == 0:
                        data['channels'][target_channel - 1]['messages'][msg_idx]['reacts'].remove(react)
                    return {}
                else:
                    # auth user has not reacted to this
                    raise InputError

    else:
        for react in data['dms'][target_dm - 1]['messages'][msg_idx]['reacts']:
            if react['react_id'] == react_id:
                #react exits
                if user['u_id'] in react['u_ids']:
                    react['u_ids'].remove(user['u_id'])
                    if len(react['u_ids']) == 0:
                        data['dms'][target_dm - 1]['messages'][msg_idx]['reacts'].remove(react)
                    return {}
                else:
                    # auth user has not reacted to this
                    raise InputError
    raise InputError

def message_pin_v1(token, message_id):
    '''
    Given a message within a channel or DM, mark it as "pinned" to be given
    special display treatment by the frontend
    Arguments:
        token (string)           - identifier unique to each user
        message_id (integer)     - identifier unique to each message

    Exceptions:
        InputError      - message_id is not a valid message
                        - Message with ID message_id is already pinned
        AccessError     - The authorised user is not a member of the channel or
                            DM that the message is within
                        - The authorised user is not an owner of the channel
                            or DM

    Return Values:
        Return {} on successful operation
    '''
    u_id = 0
    is_channel = False
    is_dm = False
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
    if u_id == 0:
        raise AccessError

    msg_found = 0
    for channel in data['channels']:
        for channel_message in channel['messages']:
            if channel_message['message_id'] == message_id:
                is_owner = False
                for owner in channel['owner_members']:
                    if owner['u_id'] == u_id:
                        is_owner = True
                if is_owner is False:
                    raise AccessError
                if channel_message['is_pinned'] == True:
                    raise InputError
                is_channel = True
                msg_found = 1
                break

    if msg_found == 0:
        for dm in data['dms']:
            for dm_message in dm['messages']:
                if dm_message['message_id'] == message_id:
                    is_owner = False
                    if dm['owner'] == u_id:
                        is_owner = True
                    if is_owner is False:
                        raise AccessError
                    if dm_message['is_pinned'] == True:
                        raise InputError
                    is_dm = True
                    msg_found = 1
                    break

    if is_channel is True:
        channel_idx = data['channels'].index(channel)
        cmsg_idx = data['channels'][channel_idx]['messages'].index(channel_message)
        data['channels'][channel_idx]['messages'][cmsg_idx]['is_pinned'] = True

    if is_dm is True:
        dm_idx = data['dms'].index(dm)
        dmsg_idx = data['dms'][dm_idx]['messages'].index(dm_message)
        data['dms'][dm_idx]['messages'][dmsg_idx]['is_pinned'] = True

    if msg_found == 0:
        raise InputError

def message_unpin_v1(token, message_id):
    '''
    Given a message within a channel or DM, remove it's mark as unpinned
    Arguments:
        token (string)           - identifier unique to each user
        message_id (integer)     - identifier unique to each message

    Exceptions:
        InputError      - message_id is not a valid message
                        - Message with ID message_id is already unpinned
        AccessError     - The authorised user is not a member of the channel or
                            DM that the message is within
                        - The authorised user is not an owner of the channel
                            or DM

    Return Values:
        Return {} on successful operation
    '''
    u_id = 0
    is_channel = False
    is_dm = False
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
    if u_id == 0:
        raise AccessError

    msg_found = 0
    for channel in data['channels']:
        for channel_message in channel['messages']:
            if channel_message['message_id'] == message_id:
                is_owner = False
                for owner in channel['owner_members']:
                    if owner['u_id'] == u_id:
                        is_owner = True
                if is_owner is False:
                    raise AccessError
                if channel_message['is_pinned'] == False:
                    raise InputError
                is_channel = True
                msg_found = 1
                break

    if msg_found == 0:
        for dm in data['dms']:
            for dm_message in dm['messages']:
                if dm_message['message_id'] == message_id:
                    is_owner = False
                    if dm['owner'] == u_id:
                        is_owner = True
                    if is_owner is False:
                        raise AccessError
                    if dm_message['is_pinned'] == False:
                        raise InputError
                    is_dm = True
                    msg_found = 1
                    break

    if is_channel is True:
        channel_idx = data['channels'].index(channel)
        cmsg_idx = data['channels'][channel_idx]['messages'].index(channel_message)
        data['channels'][channel_idx]['messages'][cmsg_idx]['is_pinned'] = False

    if is_dm is True:
        dm_idx = data['dms'].index(dm)
        dmsg_idx = data['dms'][dm_idx]['messages'].index(dm_message)
        data['dms'][dm_idx]['messages'][dmsg_idx]['is_pinned'] = False

    if msg_found == 0:
        raise InputError
