from src.data import data
from src.auth import tokenDecode
from src.error import InputError, AccessError

def notifications_get_v1(token):
    #Raise error if token doesnt exist
    for user in data['users']:
        if user['token'] == token:
            return {
                'notifications': user['notifications'][0:20],
            } 
    raise AccessError
    
def add_notification_tagged(token, msgString, id_value, id_type):
    
    '''Return the token's corresponding user id otherwise raise error if token doesn't exist'''
    user_id = user_finder(token)
    if user_id == None:
        raise AccessError

    '''Determining whether the user was invited to a channel or a dm'''
    if id_type == 'channel':
        channel_id = id_value
        dm_id = -1
    else:
        dm_id = id_value
        channel_id = -1
    
    '''Appending this notification to the beginning of the users notifications 
    if the user tagged is in the channel/dm'''
    
    for user in data['users']:
        tag = f"@{user['handle_str']}"
        if tag in msgString:
            for channel in data['channels']:
                if channel['channel_id'] == channel_id:
                    name = channel['name']
                    for member in channel['all_members']:
                        if member['u_id'] == user['u_id']:
                            user['notifications'].insert(0, {
                                'channel_id': channel_id,
                                'dm_id': dm_id,
                                'notification_message': f"{user_id['handle_str']} tagged you in {name}: {msgString[0:20]}",
                            })
                                        
            for dm in data['dms']:
                if dm['dm_id'] == dm_id:
                    name = dm['name']
                    for member in dm['members']:
                        if member['u_id'] == user['u_id']:
                            user['notifications'].insert(0, {
                                'channel_id': channel_id,
                                'dm_id': dm_id,
                                'notification_message': f"{user_id['handle_str']} tagged you in {name}: {msgString[0:20]}",
                            })
    pass
    
def add_notification_invited(token, u_ids, id_value, id_type):

    '''Return the token's corresponding user id otherwise raise error if token doesn't exist'''
    user_id = user_finder(token)
    if user_id == None:
        raise AccessError
    '''Determining whether the user was invited to a channel or a dm'''
    if id_type == 'channel':
        channel_id = id_value
        dm_id = -1
        for channel in data['channels']:
            if channel['channel_id'] == channel_id:
                name = channel['name']
                break
    else:
        dm_id = id_value
        channel_id = -1
        for dm in data['dms']:
            if dm['dm_id'] == dm_id:
                name = dm['name']
                break
    if isinstance(u_ids, list) == False: 
        for user in data['users']:
            print(user['u_id'])
            if user['u_id'] == u_ids and user['u_id'] != user_id['u_id']:
                user['notifications'].insert(0, {
                    'channel_id': channel_id,
                    'dm_id': dm_id,
                    'notification_message': f"{user_id['handle_str']} added you to {name}",
                })
    else:
        for u_id in u_ids:
            for user in data['users']:
                if user['u_id'] == u_id and user['u_id'] != user_id['u_id']:
                    user['notifications'].insert(0, {
                        'channel_id': channel_id,
                        'dm_id': dm_id,
                        'notification_message': f"{user_id['handle_str']} added you to {name}",
                    })
    pass

def add_notification_react(token, message_id, id_value, id_type):
    '''Add notification when someone reacts to a user's post'''
    user = user_finder(token)
    if user == None:
        raise AccessError
    
    channel_id = -1
    dm_id = -1
    
    if id_type == 'channel':
        channel_id = id_value
        for channel in data['channels']:
            if channel['channel_id'] == channel_id:
                for message in channel['messages']:
                    if message['message_id'] == message_id:
                        creator = uid_finder(message['u_id'])
                        creator['notifications'].insert(0, {
                            'channel_id': channel_id,
                            'dm_id': dm_id,
                            'notification_message': f"{user['handle_str']} reacted to your message in {channel['name']}",
                        })
    elif id_type == 'dm':
        dm_id = id_value
        for dm in data['dms']:
            if dm['dm_id'] == dm_id:
                for message in dm['messages']:
                    if message['message_id'] == message_id:
                        creator = uid_finder(message['u_id'])
                        creator['notifications'].insert(0, {
                            'channel_id': channel_id,
                            'dm_id': dm_id,
                            'notification_message': f"{user['handle_str']} reacted to your message in {dm['name']}",
                        })
def user_finder(token):
    for user in data['users']:
        if user['token'] == token:
            return user

def uid_finder(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return user
