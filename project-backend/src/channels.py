'''functions relating to channels'''
from src.data import data
from src.error import InputError, AccessError
import datetime
import time

def channels_list_v2(token):
    '''
    Function which lists id and name of all channels the user is a member of
    Arguments:
        Token (string)    - Identification of user
        ...

    Exceptions:
        AccessError - Occurs when token is invalid

    Return Value:
        Returns {channels} a list of channels the user is a part of

    '''

    channels = []
    u_id = 0

    for user in data['users']:
        if token == user['token']:
            u_id = user['u_id']

    if u_id == 0:
        raise AccessError

    for channel in data['channels']:
        # loop through channels
        for member in channel['all_members']:
            # loop through members
            if u_id == member['u_id']:
                # user is in channel, append details to list
                channels.append({
                    'channel_id' : channel['channel_id'],
                    'name' : channel['name']
                })

    return {"channels": channels}


def channels_listall_v2(token):
    '''
    Function which lists id and name of all channels
    Arguments:
        Token (string)    - Identification of user
        ...

    Exceptions:
        AccessError - Occurs when token is invalid

    Return Value:
        Returns {channels} a list of all channels

    '''
    channels = []
    u_id = 0

    for user in data['users']:
        if token == user['token']:
            u_id = user['u_id']

    if u_id == 0:
        raise AccessError

    for channel in data['channels']:
        # loop through channels
        channels.append({
                    'channel_id' : channel['channel_id'],
                    'name' : channel['name']
                })

    return {"channels": channels}



def channels_create_v2(token, name, is_public):
    '''
    Function used to create channels
    Arguments:
        Token (string)   - Identification of user
        name (string)    - Name given to created channel
        is_public (boolean) - Whether or not the created channel is public
        ...

    Exceptions:
        InputError  - Occurs when name is more than 20 characters long
        AccessError - Occurs when Token refers to invalid user

    Return Value:
        Returns {channel_id} for created channel

    '''

    # InputError raised when name of channel exceeds 20 characters
    if len(name) > 20:
        raise InputError

    # InputError raised when 'is_public' is neither True or False
    if is_public is not True and is_public is not False:
        raise InputError

    # InputError raised when using invalid user_id'''
    user = user_finder(token)
    if user == None:
        raise AccessError

    new_channel = {
        'channel_id': len(data['channels']) + 1,
        'name': name,
        'is_public': is_public,
        'owner_members': [],
        'all_members': [],
        'messages': [],
        'standup': {
            'time_finish': None,
            'is_active': False,
            'creator': None,
            'message_queue': [],
        },
    }

    new_channel['owner_members'].append(user)
    new_channel['all_members'].append(user)

    data['channels'].append(new_channel)

    user['channels_num'] += 1
    user['channel_time'] = int(time.time())

    return {
        'channel_id': len(data['channels'])
    }

'''HELPER FUNCTIONS'''
def user_finder(token):
    for user in data['users']:
        if user['token'] == token:
            return user
