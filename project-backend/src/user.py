import os
import sys

from flask import request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests as req
from PIL import Image
from io import BytesIO
import urllib

from src.auth import check_valid_email
from src.data import data
from src.error import InputError, AccessError
# from src.config import basedir
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def user_profile_v2(token, u_id):
    '''
    For a valid user, returns information about their 
    user_id, email, first name, last name, and handle
    Arguments:
        token (string)           - identifier unique to each user
        u_id (integer)           - identifier unique to each user
    Exceptions:
        InputError               - u_id does not refer to a valid user

    Return values:
         { user }
    '''
    input_error = 0
    uid_error = 0
    for user in data['users']:
        if user['token'] == token:
            input_error = 1
        if user['u_id'] == u_id:
            uid_error = 1

    if input_error == 0:
        raise AccessError
    if uid_error == 0:
        raise InputError

    u_id = 0
    password = ''
    email = ''
    first = ''
    last = ''
    handle = ''
    session_number = 0
    permission_id = 2
    # find user's first name and last name
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            email = user['email']
            password = user['password']
            first = user['name_first']
            last = user['name_last']
            handle = user['handle_str']
            session_number = user['session_list']
            permission_id = user['permission_id']

    return {
        'u_id': u_id,
        'email': email,
        'password': password,
        'name_first': first,
        'name_last': last,
        'handle_str': handle,
        'auth_user_id': u_id,
        'token': token,
        'session_list': session_number,
        'permission_id': permission_id
    }


def user_profile_setname_v2(token, name_first, name_last):
    '''
    Update the authorised user's first and last name
    Arguments:
        token (string)           - identifier unique to each user
        name_first               - user's first name
        name_last                - user's last name
    Exceptions:
        InputError               - name_first is not between 1 and 50 characters inclusively in length
                                 - name_last is not between 1 and 50 characters inclusively in length

    Return values:
         { user }
    '''
    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError("Name_first ...")
    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError("Name_last ...")

    for user in data['users']:
        if user['token'] == token:
            user['name_first'] = name_first
            user['name_last'] = name_last

    return {
    }


def user_profile_setemail_v2(token, email):
    '''
    Update the authorised user's email address
    Arguments:
        token (string)           - identifier unique to each user
        email                    - user's email
        name_last
    Exceptions:
        InputError               - Email entered is not a valid email
                                 - Email address is already being used by another user

    Return values:
         {}
    '''
    if not check_valid_email(email):
        raise InputError("email is not valid")
    for user in data['users']:
        if user['email'] == email:
            raise InputError("The email has been used by other user!")

    for user in data['users']:
        if user['token'] == token:
            user['email'] = email

    return {
    }


def user_profile_sethandle_v1(token, handle_str):
    '''
    Update the authorised user's handle
    Arguments:
        token (string)           - identifier unique to each user
        handle_str               - user's handle string

    Exceptions:
        InputError               - handle_str is not between 3 and 20 characters inclusive
                                 - handle is already used by another user

    Return values:
         {}
    '''
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("handle_str is not between 3 and 20 characters inclusive")
    for user in data['users']:
        if user['handle_str'] == handle_str:
            raise InputError("The handle_str has been used by other user!")

    for user in data['users']:
        if user['token'] == token:
            user['handle_str'] = handle_str

    return {
    }


def location_error_check(point, position):
    """check if the point is within position range"""
    if (point >= 0) and (point <= position):
        return False
    else:
        return True


def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Given a URL of an image on the internet, 
    crops the image within bounds (x_start, y_start) and (x_end, y_end). 
    Position (0,0) is the top left.
    Arguments:
        token (string)           - identifier unique to each user
        img_url                  - user's handle string
        x_start                  - image bounds
        y_start                  - image bounds
        x_end                    - image bounds
        y_end                    - image bounds

    Exceptions:
        InputError               - img_url returns an HTTP status other than 200.
                                 - any of x_start, y_start, x_end, y_end are 
                                   not within the dimensions of the image at the URL.
                                 - Image uploaded is not a JPG

    Return values:
         {}
    '''
    response = req.get(img_url)
    if response.status_code != 200:
        raise InputError("invalid image url...")

    img = Image.open(BytesIO(response.content))
    width = img.width
    height = img.height
    img_format = img.format

    if (x_start >= x_end) or (y_start >= y_end):
        raise InputError("location error...")
    if location_error_check(x_start, width) or location_error_check(y_start, height) \
            or location_error_check(x_end, width) or location_error_check(y_end, height):
        raise InputError("location error...")
    if (img_format.lower() != 'jpg') and (img_format.lower() != 'jpeg'):
        print(img_format.lower())
        raise InputError("image type error...")

    cropped = img.crop((x_start, y_start, x_end, y_end))
    # path = basedir + "/docs/"
    file_path = './' + token + ".jpg"
    urllib.request.urlretrieve(img_url, file_path)
    # print("============file path=============", file_path)
    cropped.save(file_path)


    for user in data['users']:
        if user['token'] == token:
            user['profile_img_url'] = file_path

    return {}


def user_stats_v1(token):
    '''
    Fetches the required statistics about this user's use of UNSW Dreams
    Arguments:
        token (string)           - identifier unique to each user

    Return values:
         { user_stats }
    '''
    num_channels_joined = 0
    num_dms_joined = 0
    num_messages_sent = 0
    channel_time_stamp = ''
    dm_time_stamp = ''
    message_time_stamp = ''

    for user in data['users']:
        if user['token'] == token:
            num_channels_joined = user['channels_num']
            num_dms_joined = user['dms_num']
            num_messages_sent = user['messages_num']
            channel_time_stamp = user['channel_time']
            dm_time_stamp = user['dm_time']
            message_time_stamp = user['message_time']

    sum_dreams = len(data['channels']) + len(data['dms']) + sum([len(channel['messages']) for channel in data['channels']])
    involvement_rate = (num_channels_joined + num_dms_joined + num_messages_sent)/sum_dreams

    return {'channels_exist': [{'num_channels_joined': num_channels_joined, 'channel_time_stamp': channel_time_stamp}],
            'dms_exist': [{'num_dms_joined':num_dms_joined, 'dm_time_stamp': dm_time_stamp}],
            'messages_exist': [{'num_messages_sent':num_messages_sent, 'message_time_stamp': message_time_stamp}],
            'involvement_rate':involvement_rate}
