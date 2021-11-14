"""contains tests for
   user_profile_v2(token, u_id)
   user_profile_setname_v2
   user_profile_setemail_v2
   user_profile_sethandle_v1"""

import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.channels import channels_create_v2
from src.user import user_profile_v2
from src.user import user_profile_setname_v2
from src.user import user_profile_setemail_v2
from src.user import user_profile_sethandle_v1
from src.user import user_profile_uploadphoto_v1
from src.user import user_stats_v1
from src.other import clear_v1
from src.error import InputError
from src.auth import auth_register_v2
from src.channel import channel_join_v2
'''test user_profile_v2'''
'''normal case'''


def test_user_profile_v2():
    clear_v1()
    user1 = auth_register_v2('hayden.everest@gmail.com', '123abc', 'Hayden', 'Everest')
    profile = user_profile_v2(user1['token'], user1['auth_user_id'])

    assert profile['u_id'] == 1
    assert profile['email'] == 'hayden.everest@gmail.com'
    assert profile['password'] == '123abc'
    assert profile['name_first'] == 'Hayden'
    assert profile['name_last'] == 'Everest'
    assert profile['handle_str'] == 'hayden.everest#1'
    assert profile['auth_user_id'] == 1
    assert profile['permission_id'] == 1


"""test user_profile_v2 Input Error"""


def test_user_profile_v2_InputError():
    clear_v1()
    user1 = auth_register_v2('john1.smith@gmail.com', 'pass123', 'John', 'Smith')
    user2 = auth_register_v2('hayden4.everest@gmail.com', '123abc', 'Hayden', 'Everest')

    invalid_u_id = 200

    with pytest.raises(InputError):
        user_profile_v2(user1['token'], invalid_u_id)
    with pytest.raises(InputError):
        user_profile_v2(user2['token'], "ThisIsAString")


# '''test user_profile_v2 Access Error'''
# def test_user_profile_v2_AccessError():
#     clear_v1()


'''test function user_profile_setname_v2'''
'''normal case'''


def test_user_profile_setname_v2():
    clear_v1()
    user4 = auth_register_v2('hayden6.everest@gmail.com', '123abc', 'Hayden', 'Everest')
    user_profile_setname_v2(user4['token'], 'John', 'Smith')
    profile = user_profile_v2(user4['token'], user4['auth_user_id'])

    # print(profile)
    answer = {'u_id': 1,
              'email': 'hayden6.everest@gmail.com',
              'password': '123abc',
              'name_first': 'John',
              'name_last': 'Smith',
              'handle_str': 'hayden.everest#1',
              'auth_user_id': 1,
              'permission_id': 1}

    assert profile['u_id'] == answer['u_id']
    assert profile['email'] == answer['email']
    assert profile['password'] == answer['password']
    assert profile['name_first'] == answer['name_first']
    assert profile['name_last'] == answer['name_last']
    assert profile['handle_str'] == answer['handle_str']
    assert profile['auth_user_id'] == answer['auth_user_id']
    assert profile['permission_id'] == answer['permission_id']


def test_user_profile_setname_v2_InputError():
    """test user_profile_v2 Input Error"""
    clear_v1()
    user1 = auth_register_v2('john.smith3@gmail.com', 'pass123', 'John', 'Smith')
    user2 = auth_register_v2('john.smith4@gmail.com', 'pass123', 'Johnn', 'Smithh')
    user3 = auth_register_v2('john.smith5@gmail.com', 'pass123', 'Johnnn', 'Smithhh')
    user4 = auth_register_v2('john.smith6@gmail.com', 'pass123', 'Johnnnn', 'Smithhhh')

    with pytest.raises(InputError):
        user_profile_setname_v2(user1['token'], 'Johnnnnnnnnohnnnnnnnnohnnnnnnnnohnnnnnnnnohnnnnnnnnnn', 'Smith')
    with pytest.raises(InputError):
        user_profile_setname_v2(user2['token'], '', 'Smith')
    with pytest.raises(InputError):
        user_profile_setname_v2(user3['token'], 'John', 'Smithnnnnnnnohnnnnnnnnohnnnnnnnnohnnnnnnnnohnnnnnnnnnn')
    with pytest.raises(InputError):
        user_profile_setname_v2(user4['token'], 'John', '')


'''test function user_profile_setname_v2'''
'''normal case'''


def test_user_profile_setemail_v2():
    clear_v1()
    user1 = auth_register_v2('john.smith6@gmail.com', 'pass123', 'John', 'Smith')

    user_profile_setemail_v2(user1['token'], 'hayden.everest@gmail.com')
    profile = user_profile_v2(user1['token'], user1['auth_user_id'])

    print(profile)
    answer = {'u_id': 1, 'email': 'hayden.everest@gmail.com', 'password': 'pass123', 'name_first': 'John',
              'name_last': 'Smith', 'handle_str': 'john.smith#1', 'auth_user_id': 1,
              'token': b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjo1NH0.WuDpHPnWs_rQXzXDu4Abz23w1kQ7KGmqwcckgZytCAA',
              'session_list': ([54],), 'permission_id': 1}

    assert profile['u_id'] == answer['u_id']
    assert profile['email'] == answer['email']
    assert profile['password'] == answer['password']
    assert profile['name_first'] == answer['name_first']
    assert profile['name_last'] == answer['name_last']
    assert profile['handle_str'] == answer['handle_str']
    assert profile['auth_user_id'] == answer['auth_user_id']
    assert profile['permission_id'] == answer['permission_id']


'''test invalid email'''


def test_user_profile_setemail_v2_InputError():
    clear_v1()
    user1 = auth_register_v2('john.smith9@gmail.com', 'pass123', 'John', 'Smith')

    with pytest.raises(InputError):
        user_profile_setemail_v2(user1['token'], '9512955.123@@_221.522')


'''test emial already used by other user'''


def test_user_profile_setemail_v2_InputError_used():
    clear_v1()
    user1 = auth_register_v2('john.smith12@gmail.com', 'pass123', 'John', 'Smith')

    with pytest.raises(InputError):
        user_profile_setemail_v2(user1['token'], 'john.smith12@gmail.com')


'''test user_profile_sethandle_v1 '''
'''normal case'''


def test_user_profile_sethandle_v1():
    clear_v1()
    user1 = auth_register_v2('john.smith12@gmail.com', 'pass123', 'John', 'Smith')

    user_profile_sethandle_v1(user1['token'], 'newhandle')
    profile = user_profile_v2(user1['token'], user1['auth_user_id'])

    answer = {'u_id': 1, 'email': 'john.smith12@gmail.com', 'password': 'pass123', 'name_first': 'John',
              'name_last': 'Smith', 'handle_str': 'newhandle', 'auth_user_id': 1,
              'token': b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjo1OH0.xuf1AMClR5elE5ZHu83pnQjwBUBK2PRGQ4g8r84Kc9E',
              'session_list': ([58],), 'permission_id': 1}
    assert profile['u_id'] == answer['u_id']
    assert profile['email'] == answer['email']
    assert profile['password'] == answer['password']
    assert profile['name_first'] == answer['name_first']
    assert profile['name_last'] == answer['name_last']
    assert profile['handle_str'] == answer['handle_str']
    assert profile['auth_user_id'] == answer['auth_user_id']
    assert profile['permission_id'] == answer['permission_id']


'''test invalid handle'''


def test_user_profile_sethandle_v1_InputError():
    clear_v1()
    user1 = auth_register_v2('john.smith3@gmail.com', 'pass123', 'John', 'Smith')
    user2 = auth_register_v2('john.smith4@gmail.com', 'pass123', 'Johnn', 'Smithh')

    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], 'john.smith#1')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user2['token'], 'john.smith#1')


'''test handle already used by other user'''


def test_user_profile_sethandle_v1_InputError_used():
    clear_v1()
    user1 = auth_register_v2('john.smith12@gmail.com', 'pass123', 'John', 'Smith')

    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], 'john.smith#1')


def test_user_stats_v1():
    clear_v1()
    user1 = auth_register_v2('john.smith12@gmail.com', 'pass123', 'John', 'Smith')
    new_channel = channels_create_v2(user1['token'], 'Channel_One', True)
    user2 = auth_register_v2('john.smith4@gmail.com', 'pass123', 'Johnn', 'Smithh')
    channel_join_v2(user2['token'], new_channel['channel_id'])
    result = user_stats_v1(user2['token'])

    assert result['channels_exist'][0]['num_channels_joined'] == 1


# def test_user_profile_uploadphoto_v1():
#     clear_v1()
#     user1 = auth_register_v2('john.smith12@gmail.com', 'pass123', 'John', 'Smith')

#     user_profile_uploadphoto_v1(user1['token'], 'https://tu1.whhost.net/uploads/20181229/10/1546049062-aTdoqIjBzl.jpg',
#                                 0, 0, 50, 50)

#     basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     assert user1['profile_img_url'] == basedir + "/docs/" + user1['token'] + ".jpeg"


# def test_user_profile_uploadphoto_httpcode_error_v1():
#     """when photo url status code is not 200"""
#     clear_v1()
#     user1 = auth_register_v2('john.smith12@gmail.com', 'pass123', 'John', 'Smith')

#     with pytest.raises(InputError):
#         user_profile_uploadphoto_v1(user1['token'], 'https://tnet/uploads/20181229/10/1546049062-aTdoqIjBzl.jpg', 0, 0, 50, 50)


def test_user_profile_uploadphoto_imagetype_error_v1():
    """when image type is not jpg"""
    clear_v1()
    user1 = auth_register_v2('john.smith12@gmail.com', 'pass123', 'John', 'Smith')

    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user1['token'], 'http://s6.sinaimg.cn/bmiddle/99547121tc7856425e2a5&amp;690',
                                    0, 0, 50, 50)


def test_user_profile_uploadphoto_photosize_error_v1():
    """when x,y position for image is not in correct range"""
    clear_v1()
    user1 = auth_register_v2('john.smith12@gmail.com', 'pass123', 'John', 'Smith')

    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user1['token'], 'https://tu1.whhost.net/uploads/20181229/10/1546049062-aTdoqIjBzl.jpg',
                                    -1, 0, 50, 50)
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user1['token'], 'https://tu1.whhost.net/uploads/20181229/10/1546049062-aTdoqIjBzl.jpg',
                                    0, -1, 50, 50)
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user1['token'], 'https://tu1.whhost.net/uploads/20181229/10/1546049062-aTdoqIjBzl.jpg',
                                    0, 0, -1, 50)
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user1['token'], 'https://tu1.whhost.net/uploads/20181229/10/1546049062-aTdoqIjBzl.jpg',
                                    0, -1, 50, -1)
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user1['token'], 'https://tu1.whhost.net/uploads/20181229/10/1546049062-aTdoqIjBzl.jpg',
                                    100, 0, 50, 50)
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user1['token'], 'https://tu1.whhost.net/uploads/20181229/10/1546049062-aTdoqIjBzl.jpg',
                                    0, 0, 100, 0)