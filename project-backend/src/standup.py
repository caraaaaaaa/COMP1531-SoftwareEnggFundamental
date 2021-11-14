from src.data import data
from src.error import InputError, AccessError
from datetime import datetime, timedelta
from src.notifications import add_notification_tagged
from threading import Timer

def standup_start_v1(token, channel_id, length):
    '''Starts a standup for the next length seconds in a channel and collates 
        all the messages sent during that time as one sent by the user who
        started the standup
    
    Arguments:
        <token> (<string>)    -<a tamper proof string to identify a user>-
        <channel_id> (<integer>)    -<a unique integer that identifies an existing channel>-
        <length> (<integer>)    -<the length of the standup period in seconds>-
        
    Exceptions:
        InputError - Occurs when the entered token, channel_id or length is invalid
        AccessError - Occurs when the corresponding user of a token is not in the channel
    
    Return value:
        Returns <{time_finish}> when input is valid
    '''
    
    #check if user token exists
    user = user_finder(token)
    if user == None:
        raise AccessError
    
    #check if channel_id exists
    channel = channel_finder(channel_id)
    if channel == None:
        raise InputError
        
    #check user is in channel    
    check_token(token, channel_id)
    
    #check if standup is already in session and if not set a new time_finish
    standup = channel['standup']
    end_time = datetime.now() + timedelta(seconds=length)
    time_finished = int(datetime.timestamp(end_time))
    
    #check if standup is already in session, otherwise create new standup
    if standup['is_active'] == True:
        raise InputError
    standup['is_active'] = True
    standup['creator'] = user
    standup['message_queue'] = []
    standup['time_finish'] = time_finished
    
    def end_standup(token, channel_id, user, channel):
        #Collapse messages into one and send notifications where necessary
        new_message = ''
        standup = channel['standup']
        for indx, message in enumerate(standup['message_queue']):
            if indx == len(standup['message_queue']) - 1:
                new_message += message
            else:
                new_message += message+'\n'
        data['message_id'] += 1
        channel['messages'].insert(0, {
            'message_id': data['message_id'],
            'u_id': user['auth_user_id'],
            'message': new_message,
            'time_created': int(datetime.timestamp(datetime.now())),
            'reacts': [],
            'is_pinned': False, 
        })
        
        #add notification to all tagged users
        for user in data['users']:
            tag = f"@{user['handle_str']}"
            if tag in new_message:
                name = channel['name']
                for member in channel['all_members']:
                    if member['u_id'] == user['u_id']:
                        user['notifications'].insert(0, {
                            'channel_id': channel_id,
                            'dm_id': -1,
                            'notification_message': f"{user['handle_str']} tagged you in {name}: {new_message[0:20]}",
                        })
        standup['is_active'] = False
        standup['creator'] = None
        standup['message_queue'].clear()
        standup['time_finish'] = None

    
    t_until_end = time_finished - datetime.timestamp(datetime.now())
    t = Timer(t_until_end, end_standup, args=[token, channel_id, user, channel])
    t.start()
    return {
        'time_finish': time_finished,
    }
    
def standup_active_v1(token, channel_id):
    '''Checks whether the standup is active and if so returns the time it finishes
    
    Arguments:
        <token> (<string>)    -<a tamper proof string to identify a user>-
        <channel_id> (<integer>)    -<a unique integer that identifies an existing channel>-
        
    Exceptions:
        InputError - Occurs when the entered token or channel_id is invalid
    
    Return value:
        Returns <{is_active, time_finish}> when input is valid
        Returns <{is_active: True, time_finish: None}> when no standup is active
    '''

    #check token exists
    user = user_finder(token)
    if user == None:
        raise AccessError
    
    #check if channel exists
    channel = channel_finder(channel_id)
    if channel == None:
        raise InputError
        
    #check user token is in channel
    check_token(token, channel_id)
    standup = channel['standup']
    
    #check if standup is active
    
    return {
        'is_active': standup['is_active'], 
        'time_finish': standup['time_finish'],
    }
    
def standup_send_v1(token, channel_id, message):
    '''Sends messages during the standup period to get buffered in the standup queue
    
    Arguments:
        <token> (<string>)    -<a tamper proof string to identify a user>-
        <channel_id> (<integer>)    -<a unique integer that identifies an existing channel>-
        <message> (<string>)    -<the message the user wants to send>-
        
    Exceptions:
        InputError - Occurs when the entered token, channel_id or message is invalid and when there is no active standup in session
        AccessError - Occurs when the corresponding user of a token is not in the channel
    
    Return value:
        Returns {} when input is valid
    '''
    #check if token exists
    user = user_finder(token)
    if user == None:
        raise AccessError
    
    #check if channel exists
    channel = channel_finder(channel_id)
    if channel == None:
        raise InputError
        
    #check if user token is a member of the channel
    check_token(token, channel_id)
    
    #check if message is less than 1000 characters
    if len(message) > 1000:
        raise InputError
    
    #check if standup session is active
    standup = channel['standup']
    if standup['is_active'] is not True:
        raise InputError
    #append message to message queue with the user first name
    standup['message_queue'].append(user['name_first']+': '+message)
    return {}
    
'''HELPER FUNCTIONS'''
def user_finder(token):
    for user in data['users']:
        if user['token'] == token:
            return user

def channel_finder(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel

def check_token(token, channel_id):
    valid_id = False
    channel = channel_finder(channel_id)
    for member in channel['all_members']:
        if member['token'] == token:
            valid_id = True
    if valid_id == False:
        raise AccessError

def time_finder(channel_id):
    standup = channel_finder(channel_id)['standup']
    return standup['time_finish']
