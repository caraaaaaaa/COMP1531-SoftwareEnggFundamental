import pytest

from src.data import data
from src.error import InputError, AccessError
from src.auth import tokenDecode
def clear_v1():
    data['users'].clear()
    data['channels'].clear()
    data['dms'].clear()
    data['message_id'] = 0
    return {}

def search_v2(token, query_str):
    '''Collate all messages that contain the given query string'''
    #raise input error if user does not exist with given token
    user = user_finder(token)
    if user == None:
        raise AccessError
    
    #raise input error if start is greater than 1000 characters
    if len(query_str) > 1000:
        raise InputError

    '''Declaring appendable empty list'''
    searchList = []
    
    '''Search through the user's dms first'''
    for dm in data['dms']:
        for member in dm['members']:
            if member['u_id'] == user['u_id']:
                for message in dm['messages']:
                    if query_str in message['message']:
                        searchList.append(message)

    '''Afterward, search through the user's channels next'''    
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == user['u_id']:
                for message in channel['messages']:
                    if query_str in message['message']:
                        searchList.append(message)

    return {
        'messages': searchList,
    }

def user_finder(token):
    for user in data['users']:
        if token == user['token']:
            return user
