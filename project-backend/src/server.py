from json import dumps
from flask import Flask, request
from flask_cors import CORS
from PIL import Image

import sys
import os
src_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(src_path)
sys.path.append(project_path)

from src import config
from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.error import InputError
from src.channel import channel_details_v2, channel_messages_v2, channel_removeowner_v1, channel_addowner_v1, channel_leave_v1, channel_invite_v2, channel_join_v2
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.message import message_edit_v2, message_remove_v1, message_send_v2, message_senddm_v1, message_share_v1, message_sendlater_v1, message_sendlaterdm_v1, message_react_v1, message_unreact_v1, message_pin_v1, message_unpin_v1
from src.other import clear_v1, search_v2
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.users import users_all_v1, users_stats_v1
from src.user import user_profile_sethandle_v1, user_profile_setname_v2, user_profile_setemail_v2, user_profile_v2, \
    user_profile_uploadphoto_v1, user_stats_v1
from src.dm import dm_create_v1, dm_details_v1, dm_invite_v1, dm_remove_v1, dm_leave_v1, dm_messages_v1, dm_list_v1
from src.notifications import notifications_get_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/user/profile/v2", methods=['GET'])
def http_user_profile_v2():
    data = request.get_json()
    token = data.get("token")
    u_id = data.get("u_id")
    res = user_profile_v2(token=token, u_id=u_id)
    return res


@APP.route("/user/setname/v2", methods=['PUT'])
def profile_setname():
    data = request.get_json()
    token = data.get("token")
    name_first = data.get("name_first")
    name_last = data.get("name_last")

    return user_profile_setname_v2(token, name_first, name_last)


@APP.route("/user/setemail/v2", methods=['PUT'])
def profile_setemail():
    data = request.get_json()
    token = data.get("token")
    email = data.get("email")

    return user_profile_setemail_v2(token, email)


@APP.route("/user/sethandle/v2", methods=['PUT'])
def profile_sethandle():
    data = request.get_json()
    token = data.get("token")
    handle_str = data.get("handle_str")

    return user_profile_sethandle_v1(token, handle_str)


@APP.route('/clear/v1', methods=['DELETE'])
def http_clear_v1():
    return dumps(clear_v1())

# AUTH
@APP.route('/auth/login/v2', methods=['POST'])
def http_auth_login():
    '''
    Wrapper function for auth/login/v1
    '''
    payload = request.get_json()
    return dumps(auth_login_v2(payload['email'],
                                payload['password']))


@APP.route('/auth/register/v2', methods=['POST'])
def http_auth_register():
    '''
    Wrapper function for auth/register/v1
    '''
    payload = request.get_json()
    return dumps(auth_register_v2(payload['email'],
                                payload['password'],
                                payload['name_first'],
                                payload['name_last']))

@APP.route('/auth/logout/v1', methods=['POST'])
def http_auth_logout():
    '''
    Wrapper function for auth/logout/v1
    '''
    payload = request.get_json()
    return dumps(auth_logout_v1(payload['token']))

@APP.route('/auth/passwordreset/request/v1', methods=['POST'])
def http_auth_passwordreset_request():
    '''
    Wrapper function for auth/passwordeset/request
    '''
    payload = request.get_json()
    return dumps(auth_passwordreset_request_v1(payload['email']))
                                
@APP.route('/auth/passwordreset/reset/v1', methods=['POST'])
def http_auth_passwordreset_reset():
    '''
    Wrapper function for auth/passwordreset/reset
    '''
    payload = request.get_json()
    return dumps(auth_passwordreset_reset_v1(payload['reset_code'], payload['new_password']))

# ADMIN
@APP.route('/admin/user/remove/v1', methods=['DELETE'])
def http_admin_user_remove():
    '''
    Wrapper function for admin/user/remove/v1
    '''
    payload = request.get_json()
    return dumps(admin_user_remove_v1(payload['token'],
                                      payload['u_id']))

@APP.route('/admin/userpermission/change/v1', methods=['POST'])
def http_admin_userpermission_change():
    '''
    Wrapper function for admin/userpermission/change/v1
    '''
    payload = request.get_json()
    return dumps(admin_userpermission_change_v1(payload['token'],
                                      payload['u_id'],
                                      payload['permission_id']))

# CHANNEL
@APP.route('/channel/details/v2', methods=['GET'])
def http_channel_details():
    '''
    Wrapper function for channel/details/v2
    '''
    payload = request.get_json()
    return dumps(channel_details_v2(payload['token'],
                                    payload['channel_id']))

@APP.route('/channel/messages/v2', methods=['GET'])
def http_channel_messages():
    '''
    Wrapper function for channel/messages/v2
    '''
    payload = request.get_json()
    return dumps(channel_messages_v2(payload['token'],
                                     payload['channel_id'],
                                     payload['start']))

@APP.route('/channel/addowner/v1', methods=['POST'])
def http_channel_addowner():
    '''
    Wrapper function for channel/addowner/v1
    '''
    payload = request.get_json()
    return dumps(channel_addowner_v1(payload['token'],
                                     payload['channel_id'],
                                     payload['u_id']))

@APP.route('/channel/removeowner/v1', methods=['DELETE'])
def http_channel_removeowner():
    '''
    Wrapper function for channel/removeowner/v1
    '''
    payload = request.get_json()
    return dumps(channel_removeowner_v1(payload['token'],
                                     payload['channel_id'],
                                     payload['u_id']))

@APP.route('/channel/leave/v1', methods=['POST'])
def http_channel_leave():
    '''
    Wrapper function for channel/leave/v1
    '''
    payload = request.get_json()
    return dumps(channel_leave_v1(payload['token'],
                                    payload['channel_id']))

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    data = request.get_json()
    token = data.get("token")
    channel_id = data.get("channel_id")
    u_id = data.get("u_id")
    res = channel_invite_v2(token=token, channel_id=channel_id, u_id=u_id)
    return res


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    data = request.get_json()
    token = data.get("token")
    channel_id = data.get("channel_id")
    res = channel_join_v2(token=token, channel_id=channel_id)
    return res





# Message
@APP.route('/message/send/v2', methods=['POST'])
def http_message_send():
    '''
    Wrapper function for message send
    '''
    payload = request.get_json()
    return dumps(message_send_v2(payload['token'],
                                payload['channel_id'],
                                payload['message']))

@APP.route('/message/edit/v2', methods=['PUT'])
def http_message_edit():
    '''
    Wrapper function for message edit
    '''
    payload = request.get_json()
    return dumps(message_edit_v2(payload['token'],
                                payload['message_id'],
                                payload['message']))

@APP.route('/message/remove/v1', methods=['DELETE'])
def http_message_remove():
    '''
    Wrapper function for message remove
    '''
    payload = request.get_json()
    return dumps(message_remove_v1(payload['token'],
                                payload['message_id']))

@APP.route('/message/share/v1', methods=['POST'])
def http_message_share():
    '''
    Wrapper function for message share
    '''
    payload = request.get_json()
    return dumps(message_share_v1(payload['token'],
                                payload['og_message_id'],
                                payload['message'],
                                payload['channel_id'],
                                payload['dm_id']))

@APP.route('/message/senddm/v1', methods=['POST'])
def http_message_senddm():
    '''
    Wrapper function for message send dm
    '''
    payload = request.get_json()
    return dumps(message_senddm_v1(payload['token'],
                                payload['dm_id'],
                                payload['message']))

@APP.route('/message/sendlater/v1', methods=['POST'])
def http_message_sendlater():
    '''
    Wrapper function for message send later
    '''
    payload = request.get_json()
    return dumps(message_sendlater_v1(payload['token'],
                                payload['channel_id'],
                                payload['message'],
                                payload['time_sent']))

@APP.route('/message/sendlaterdm/v1', methods=['POST'])
def http_message_sendlaterdm():
    '''
    Wrapper function for message send later dm
    '''
    payload = request.get_json()
    return dumps(message_sendlaterdm_v1(payload['token'],
                                payload['dm_id'],
                                payload['message'],
                                payload['time_sent']))

@APP.route('/message/react/v1', methods=['POST'])
def http_message_react():
    '''
    Wrapper function for message react
    '''
    payload = request.get_json()
    return dumps(message_react_v1(payload['token'],
                                payload['message_id'],
                                payload['react_id']))

@APP.route('/message/unreact/v1', methods=['POST'])
def http_message_unreact():
    '''
    Wrapper function for message unreact
    '''
    payload = request.get_json()
    return dumps(message_unreact_v1(payload['token'],
                                payload['message_id'],
                                payload['react_id']))

@APP.route('/message/pin/v1', methods=['POST'])
def http_message_pin():
    '''
    Wrapper function for message pin
    '''
    payload = request.get_json()
    return dumps(message_pin_v1(payload['token'],
                                payload['message_id']))

@APP.route('/message/unpin/v1', methods=['POST'])
def http_message_unpin():
    '''
    Wrapper function for message unpin
    '''
    payload = request.get_json()
    return dumps(message_unpin_v1(payload['token'],
                                  payload['message_id']))

# CHANNELS
@APP.route('/channels/list/v2', methods=['GET'])
def http_channels_list():
    '''
    Wrapper function for channels list
    '''
    payload = request.get_json()
    return dumps(channels_list_v2(payload['token']))

@APP.route('/channels/listall/v2', methods=['GET'])
def http_channels_listall():
    '''
    Wrapper function for channels list all
    '''
    payload = request.get_json()
    return dumps(channels_listall_v2(payload['token']))

@APP.route('/channels/create/v2', methods=['POST'])
def http_channels_create():
    '''
    Wrapper function for channels create
    '''
    payload = request.get_json()
    return dumps(channels_create_v2(payload['token'],
                               payload['name'],
                               payload['is_public']))

# USERS
@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    data = request.get_json()
    token = data.get("token")
    res = users_all_v1(token=token)
    return res

# DMS
@APP.route("/dm/invite/v1", methods=['POST'])
def http_dm_invite_v1():

    payload = request.get_json()
    return dumps(dm_invite_v1(payload['token'], payload['dm_id'], payload['u_id']))

@APP.route("/dm/leave/v1", methods=['POST'])
def http_dm_leave_v1():

    payload = request.get_json()
    return dumps(dm_leave_v1(payload['token'], payload['dm_id']))

@APP.route("/dm/messages/v1", methods=['GET'])
def http_dm_messages_v1():

    payload = request.get_json()
    return dumps(dm_messages_v1(payload['token'], payload['dm_id'], payload['start']))


@APP.route("/dm/create/v1", methods=['POST'])
def http_dm_create_v1():

    payload = request.get_json()
    return dumps(dm_create_v1(payload['token'], payload['u_ids']))

@APP.route("/dm/details/v1", methods=['GET'])
def http_dm_details_v1():
    payload = request.get_json()
    return dumps(dm_details_v1(payload['token'], payload['dm_id']))

@APP.route("/dm/list/v1", methods=['GET'])
def http_dm_list_v1():
    payload = request.get_json()
    return dumps(dm_list_v1(payload['token']))

@APP.route("/dm/remove/v1", methods=['DELETE'])
def http_dm_remove_v1():
    payload = request.get_json()
    return dumps(dm_remove_v1(payload['token'], payload['dm_id']))

# SEARCH
@APP.route("/search/v2", methods=['GET'])
def http_search_v2():

    payload = request.get_json()
    return dumps(search_v2(payload['token'], payload['query_str']))

# NOTIFICATIONS
@APP.route("/notifications/get/v1", methods=['GET'])
def http_notifications_get_v1():
    payload = request.get_json()
    return dumps(notifications_get_v1(payload['token']))


@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def http_profile_uploadphoto_v1():
    payload = request.get_json()
    print(payload)
    return dumps(user_profile_uploadphoto_v1(payload['token'], 
                                             payload['img_url'],
                                             payload['x_start'],
                                             payload['y_start'],
                                             payload['x_end'],
                                             payload['y_end']
                                            ))


# user_stats_v1
@APP.route("/user/stats/v1", methods=['GET'])
def http_user_stats_v1():
    payload = request.get_json()
    return dumps(user_stats_v1(payload['token']))


# user_stats_v1
@APP.route("/users/stats/v1", methods=['GET'])
def http_users_stats_v1():
    payload = request.get_json()
    return dumps(users_stats_v1(payload['token']))


# STANDUP
@APP.route("/standup/start/v1", methods=['POST'])
def http_standup_start_v1():
    payload = request.get_json()
    return dumps(standup_start_v1(payload['token'], payload['channel_id'], payload['length']))

@APP.route("/standup/active/v1", methods=['GET'])
def http_standup_active_v1():
    payload = request.get_json()
    return dumps(standup_active_v1(payload['token'], payload['channel_id']))

@APP.route("/standup/send/v1", methods=['POST'])
def http_standup_send_v1():
    payload = request.get_json()
    return dumps(standup_send_v1(payload['token'], payload['channel_id'], payload['message']))


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
