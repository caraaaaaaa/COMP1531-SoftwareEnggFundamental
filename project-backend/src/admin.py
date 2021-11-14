'''Functions relating to channel'''
from src.data import data
from src.error import InputError, AccessError

def admin_user_remove_v1(token, u_id):
    '''
    Given a User by their user ID, remove the user from the Dreams. Dreams
    owners can remove other **Dreams** owners
    Arguments:
        token (string)           - identifier unique to each user
        u_id (integer)           - identifier unique to each user

    Exceptions:
        InputError      - u_id does not refer to a valid user
                        - The user is currently the only owner
        AccessError     - The authorised user is not an owner

    Return Values:
        Return {} on successful operation
    '''
    # Checks if entered id is valid
    user = user_finder(token)
    if user is None:
        raise AccessError
    user = user_finder_from_u_id(u_id)
    if user is None:
        raise InputError

    # Checks if the remover is the owner
    for user in data['users']:
        if token == user['token']:
            if user['permission_id'] != 1:
                raise AccessError

    # Checks if removing the only owner
    owner_count = 0
    for user in data['users']:
        if user['permission_id'] == 1:
            owner_count += 1
    if owner_count <= 1:
        # Checks if the user to be removed is an owner
        for user in data['users']:
            if u_id == user['u_id']:
                owner = user
                if owner['permission_id'] == 1:
                    raise InputError



    # Changes the contents of all messages by this user to 'Removed User'
    for dm in data['dms']:
        for message in dm['messages']:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'
    for channel in data['channels']:
        for message in channel['messages']:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'

    # Removes user from Dreams
    for user in data['users']:
        if u_id == user['u_id']:
            # data['users'].remove(user)
            user['name_first'] = 'Removed user'
            user['name_last'] = 'Removed user'
            break

def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    Given a User by their user ID, set their permissions to new permissions
    described by permission_id
    Arguments:
        token (string)           - identifier unique to each user
        u_id (integer)           - identifier unique to each user
        permission_id (integer ) - identifier unique to each permission

    Exceptions:
        InputError      - u_id does not refer to a valid user
                        - permission_id does not refer to a value permission
        AccessError     - The authorised user is not an owner

    Return Values:
        Return {} on successful operation
    '''
    permission_id_list = [1, 2]

    # Checks if entered id is valid
    user = user_finder(token)
    if user is None:
        raise InputError
    user = user_finder_from_u_id(u_id)
    if user is None:
        raise InputError

    # Checks if valid permission id
    if permission_id not in permission_id_list:
        raise InputError

    # Checks if the auth_user is the owner
    for user in data['users']:
        if token == user['token']:
            if user['permission_id'] == 1:
                break
            else:
                raise AccessError

    for user in data['users']:
        if u_id == user['u_id']:
            user['permission_id'] =  permission_id

def user_finder(token):
    for user in data['users']:
        if token == user['token']:
            return user

def user_finder_from_u_id(u_id):
    for user in data['users']:
        if u_id == user['u_id']:
            return user

