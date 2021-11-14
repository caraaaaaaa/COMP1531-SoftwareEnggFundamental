'''DM functions'''
import jwt
from src.data import data
from src.error import InputError, AccessError
from datetime import datetime, timezone
from src.auth import *
from src.notifications import add_notification_invited
def dm_invite_v1(token, dm_id, u_id):
    '''Function allows users in dms to invite users who aren't'''
    auth_user_id = user_finder(token)
    if auth_user_id == None:
        raise AccessError
    '''Raise error if token or dm is invalid'''
    check_token_dm(token, dm_id)
    '''Raise error if invited user is invalid'''
    auth_user_id = token_check(token)['u_id']
    validUser = 0
    for user in data['users']:
        if user['u_id'] == u_id:
            validUser = 1
            break

    if auth_user_id == u_id:
        raise InputError
    if validUser == 0:
        raise InputError

    indx = dm_finder(dm_id)

    for user in data['users']:
        if user['u_id'] == u_id:
            u_id = user['u_id']
            email = user['email']
            first_name = user['name_first']
            last_name = user['name_last']
            handle_str = user['handle_str']

    userInfo = {
        'u_id': u_id,
        'email': email,
        'name_first': first_name,
        'name_last': last_name,
        'handle_str': handle_str,
    }
    '''append user info to members list of dm'''

    data['dms'][indx]['members'].append(userInfo)
    add_notification_invited(token, u_id, dm_id, 'dm')
    return {}

def dm_list_v1(token):

    # list to store details of the user
    dm_list = []
    user = user_finder(token)
    if user == None:
        raise AccessError
    #Find user in members and add the dm_id and name of dm to the user_dm_list

    try:
        checked_token = token_check(token)
        if checked_token == {}:
            raise AccessError("User id is not verified")
    except InputError as err:
        raise AccessError("User id not verified!") from err
    for dm in data['dms']:
        if dm == {}:
            return {'dms' : dm_list}

        for member in dm['members']:
            if checked_token['u_id'] == member['u_id']:
                dm_list.append({'dm_id' : dm['dm_id'], 'name' : dm['name']})

    return {'dms' : dm_list}

def dm_leave_v1(token, dm_id):
    '''Function allows users in dms to leave'''
    '''Raise error if token or dm_id is invalid'''
    check_token_dm(token, dm_id)
    auth_user_id = user_finder(token)['u_id']
    indx = dm_finder(dm_id)
    member_indx = member_finder(dm_id, auth_user_id)
    '''Remove user information from the members list for the given dm information'''
    data['dms'][indx]['members'].pop(member_indx)

    return {}


def dm_create_v1(token, u_ids):

    #check token is valid
    #valid_token(token)

    #find auth_user_id for session
    user = user_finder(token)

    #check for the InputError

    if user == None:
        raise AccessError   #u_id does not refer to a valid user

    #check if u_ids is valid
    if isinstance(u_ids, list) == False:
        raise InputError
    if len(u_ids) != 0:
        count = 0
        for u_id in u_ids:
            if u_id == user['u_id']:
                raise InputError
            for users in data['users']:
                if u_id == users['u_id']:
                    count += 1
                    break
        if count != len(u_ids):
            raise InputError

    #create a dm_id
    current_users = data['dms']
    current_id = (len(current_users) + 1)

    #create a dm_name
    owner_id = user['u_id']
    u_ids.append(owner_id)
    members = u_ids


    dm_name = []

    newMembers = []

    for uid in members:
        for user in data['users']:
            if user['u_id'] == uid:
                name = user['handle_str']
                dm_name.append(name)
                dm_name = sorted(dm_name)
                info = {
                    'u_id': user['u_id'],
                    'email': user['email'],
                    'name_first': user['name_first'],
                    'name_last': user['name_last'],
                    'handle_str': user['handle_str'],
                }
                newMembers.append(info)
    dm_name = ",".join(dm_name)


    dm = {
        'dm_id' : current_id,
        'name': dm_name,
        'messages' : [],
        'owner' : owner_id,
        'members' : newMembers
        }

    data['dms'].append(dm)

    add_notification_invited(token, u_ids, current_id, 'dm')
    return {'dm_id' : current_id, 'dm_name' : dm_name}

def dm_details_v1(token, dm_id):

    #check if dm_id is valid or not

    user = user_finder(token)

    if user == None:
        raise AccessError

    if dm_id_valid(dm_id) == False:
        raise InputError  # Dm id is not a valid dm


    in_list = False
    dm_list = dm_list_v1(token)
    for dm in dm_list['dms']:
        if dm['dm_id'] == dm_id:
            in_list = True
    if in_list == False:
        raise AccessError  # Authorised user is not a member of this DM with dm_id

    # finds the dm and returns name and members

    for dm in data['dms']:
        if dm.get('dm_id') == dm_id:

            name = dm.get('name')
            members = dm.get('members')
            break

    return {
        'name' : name,
        'members' : members
    }                                # Returns names and members

def dm_remove_v1(token, dm_id):

    #check if token exists
    user = user_finder(token)
    if user == None:
        raise AccessError
    #check token is valid
    checked_token = token_check(token)

    #check for valid dm_id

    dm_id_valid(dm_id)

    is_verified = False
    for dm in data['dms']:
        if dm['owner'] == checked_token['u_id'] :
            is_verified = True
    if is_verified == False:
        raise AccessError     # The user is not the dm creator

    #removes the existing dm
    for dm in data['dms']:

        if dm['dm_id'] == dm_id:
            dm.clear()               #Remove the existing dm

    return {}



def dm_messages_v1(token, dm_id, start):

    '''Raise error if token or dm is invalid'''
    #check if token and dm are invalid
    check_token_dm(token, dm_id)
    indx = dm_finder(dm_id)
    messages = data['dms'][indx]['messages']
    '''Raise error if start is greater than number of messages - 1'''
    if isinstance(start, int) == False:
        raise InputError
    if start > len(messages):
        raise InputError

    end = start + 50
    if len(messages) - start < 51:
        stopper = len(messages) - start
        end = -1
    else:
        stopper = end

    newMessages = []

    counter = start
    while counter < stopper:
        newMessages.append(messages[counter])
        counter += 1
    return {
        'messages': newMessages,
        'start': start,
        'end': end,
    }


def messageList(NumberOfMessages):
    counter = 0
    messages = []
    while counter < NumberOfMessages:
        messages.append(str(counter + 1))
        counter += 1
    return messages

def dm_finder(dm_id):
    indx = 0
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            return indx
        indx += 1

def handle_finder(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return user['handle_str']

def member_finder(dm_id, u_id):
    indx = dm_finder(dm_id)
    counter = 0
    for member in data['dms'][indx]['members']:
        if member['u_id'] == u_id:
            return counter
        counter += 1

def valid_token(token):
    '''Raise error if token doesn't exist'''
    validToken = 0
    session_id = tokenDecode(token)['session_id']
    for user in data['users']:
        for session in user['session_list']:
            if session == session_id:
                validToken = 1
    if validToken == 0:
        raise AccessError


def check_token_dm(token, dm_id):
    '''Raise error if token doesn't exist'''
    auth_user_id = user_finder(token)
    if auth_user_id == None:
        raise AccessError
    '''Check dm entered is valid'''
    check_dm(dm_id)
    '''Raise error if user of token is not in the dm'''
    indx = dm_finder(dm_id)
    validToken = list(filter(lambda a: a['u_id'] == auth_user_id['u_id'], data['dms'][indx]['members']))
    if len(validToken) == 0:
        raise AccessError

def check_dm(dm_id):
    '''Raise error if dm_id is invalid'''
    validDm = list(filter(lambda a: a['dm_id'] == dm_id, data['dms']))
    if len(validDm) == 0:
        raise InputError

def dm_id_valid(dm_id):

    dm_is_valid = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            dm_is_valid = True

    if dm_is_valid == False:
        raise InputError    # dm id is not valid

def search_time_created(dm_id, message_id):
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    return message['time_created']

# Checks if the user is part of dm

def user_part_dm(token,dm_id):

    in_list = False
    dm_list = dm_list_v1(token)
    for dm in dm_list['dms']:
        if dm['dm_id'] == dm_id:
            in_list = True
    if in_list == False:
        raise AccessError ("User is not in dm")

def user_finder(token):
    for user in data['users']:
        if token == user['token']:
            return user
