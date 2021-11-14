from src.data import data


def users_all_v1(token):
    '''
    Returns a list of all users and their associated details
    Arguments:
        token (string)           - identifier unique to each user

    Return values:
         { users }
    '''
    return {'users': data['users']}


def users_stats_v1(token):
    '''
    Fetches the required statistics about the use of UNSW Dreams
    Arguments:
        token (string)           - identifier unique to each user

    Return values:
         { dreams_stats }
    '''
    num_channels_exist = len(data['channels'])      
    num_dms_exist = len(data['dms'])                
    num_messages_exist = 0                         
    utilization_users_list = []
    for channel in data['channels']:
        num_messages_exist += len(channel['messages'])      # message sum of channels
        utilization_users_list.extend([member['u_id'] for member in channel['all_members']])
        print(utilization_users_list)
    for dm in data['dms']:
        num_messages_exist += len(dm['messages'])          # message sum of (channels and dms)
        utilization_users_list.extend([member['u_id'] for member in dm['members']])
    print(utilization_users_list)
    
    num_utilization_use = len(set(utilization_users_list))
    utilization_rate = num_utilization_use / len(data['users'])

    channel_time_list = []
    dm_time_list = []
    message_time_list = []
    for user in data['users']:
        channel_time_list.append(user['channel_time'])
        dm_time_list.append(user['dm_time'])
        message_time_list.append(user['message_time'])

    channel_time_stamp = max(channel_time_list)
    dm_time_stamp = max(dm_time_list)
    message_time_stamp = max(message_time_list)

    return {'channels_exist': [{'num_channels_exist': num_channels_exist, 'time_stamp': channel_time_stamp}],
            'dms_exist': [{'num_dms_exist': num_dms_exist, 'time_stamp': dm_time_stamp}],
            'messages_exist': [{'num_messages_exist': num_messages_exist, 'message_time_stamp': message_time_stamp}],
            'utilization_rate': utilization_rate
            }