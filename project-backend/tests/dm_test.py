import pytest
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError, AccessError
from src.channels import channels_create_v2
from src.other import clear_v1
from src.dm import *
from src.message import message_senddm_v1
from datetime import timezone

'''
sample dms data base:
{
    'dms': [{
        'name':,
        'messages':[
            'message_id':,
            'u_id':,
            'message':,
            'time_created':,
        ],
        'members':,
    }]
}
'''
def message_list(numberMessages):
    emptyList = []
    counter = 0
    while counter < numberMessages:
        emptyList.append('1')
        counter += 1
    if len(emptyList) == numberMessages:
        return emptyList
    else:
        return None

'''Tests for dm_invite_v1()'''

def test_dm_invite():
    '''Test basic functionality'''
    clear_v1()

    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    member2 = auth_register_v2('jake.smith@gmail.com', 'pass123', 'Jake', 'Smith')
    members = [member1['auth_user_id']]
    dm = dm_create_v1(owner['token'], members)
    dm_invite = dm_invite_v1(owner['token'], dm['dm_id'], member2['auth_user_id'])

    assert dm_invite == {}

    dm_details = dm_details_v1(owner['token'], dm['dm_id'])

    assert len(dm_details['members']) == 3


def test_dm_invite_invalid_token():
    '''test for invalid token'''
    clear_v1()

    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    member2 = auth_register_v2('jake.smith@gmail.com', 'pass123', 'Jake', 'Smith')
    non_member1 = auth_register_v2('bake.smith@gmail.com', 'pass123', 'Bake', 'Smith')
    non_member2 = auth_register_v2('cake.smith@gmail.com', 'pass123', 'Cake', 'Smith')
    non_member3 = auth_register_v2('fake.smith@gmail.com', 'pass123', 'Fake', 'Smith')
    members = [member1['auth_user_id']]
    dm = dm_create_v1(owner['token'], members)

    with pytest.raises(AccessError):
        dm_invite_v1(0, dm['dm_id'], member2['auth_user_id'])
    with pytest.raises(AccessError):
        dm_invite_v1({}, dm['dm_id'], member2['auth_user_id'])
    with pytest.raises(AccessError):
        dm_invite_v1(non_member1['token'], dm['dm_id'], member2['auth_user_id'])
    with pytest.raises(AccessError):
        dm_invite_v1(non_member2['token'], dm['dm_id'], member2['auth_user_id'])
    with pytest.raises(AccessError):
        dm_invite_v1(non_member3['token'], dm['dm_id'], member2['auth_user_id'])

def test_dm_invite_invalid_user():
    '''Test for invalid user id'''

    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    member2 = auth_register_v2('jake.smith@gmail.com', 'pass123', 'Jake', 'Smith')
    members = [member1['auth_user_id']]
    dm = dm_create_v1(owner['token'], members)

    with pytest.raises(InputError):
        dm_invite_v1(owner['token'], dm['dm_id'], 0)
    with pytest.raises(InputError):
        dm_invite_v1(owner['token'], dm['dm_id'], str(member2['auth_user_id']))
    with pytest.raises(InputError):
        dm_invite_v1(owner['token'], dm['dm_id'], {})

def test_dm_invite_invalid_dm():
    '''Test for invalid dm id'''

    clear_v1()
    owner1 = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    owner2 = auth_register_v2('jake.smith@gmail.com', 'pass123', 'Jake', 'Smith')
    members = [member1['auth_user_id']]
    dm_create_v1(owner1['token'], members)
    dm = dm_create_v1(owner2['token'], members)

    with pytest.raises(InputError):
        dm_invite_v1(owner1['token'], 0, owner2['auth_user_id'])
    with pytest.raises(InputError):
        dm_invite_v1(owner1['token'], str(dm['dm_id']), owner2['auth_user_id'])
    with pytest.raises(InputError):
        dm_invite_v1(owner1['token'], {}, owner1['auth_user_id'])

'''Tests for dm_leave_v1()'''

def test_dm_leave():
    '''Test basic functionality'''

    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    members = [member1['auth_user_id']]
    dm = dm_create_v1(owner['token'], members)
    dm_leave = dm_leave_v1(member1['token'], dm['dm_id'])
    dm_details = dm_details_v1(owner['token'], dm['dm_id'])

    assert dm_leave == {}
    assert len(dm_details['members']) == 1

def test_dm_leave_invalid_token():
    '''Test for invalid token'''

    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    non_member1 = auth_register_v2('jake.smith@gmail.com', 'pass123', 'Jake', 'Smith')
    non_member2 = auth_register_v2('fake.smith@gmail.com', 'pass123', 'Fake', 'Smith')
    members = [member1['auth_user_id']]
    dm = dm_create_v1(owner['token'], members)

    with pytest.raises(AccessError):
        dm_leave_v1(0, dm['dm_id'])
    with pytest.raises(AccessError):
        dm_leave_v1({}, dm['dm_id'])
    with pytest.raises(AccessError):
        dm_leave_v1(non_member1['token'], dm['dm_id'])
    with pytest.raises(AccessError):
        dm_leave_v1(non_member2['token'], dm['dm_id'])

def test_dm_leave_invalid_user():
    '''Test for invalid user'''

    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    members = [member1['auth_user_id']]
    dm = dm_create_v1(owner['token'], members)

    with pytest.raises(InputError):
        dm_leave_v1(owner['token'], 0)
    with pytest.raises(InputError):
        dm_leave_v1(owner['token'], str(dm['dm_id']))
    with pytest.raises(InputError):
        dm_leave_v1(owner['token'], {})

'''Test for dm_messages_v1()'''

def test_simple_dm_messages():
    #Test basic functionality

    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    members = [member1['auth_user_id']]
    dm = dm_create_v1(owner['token'], members)
    msgString = 'How are you?'
    message_senddm_v1(owner['token'], dm['dm_id'], msgString)
    dm_messages = dm_messages_v1(owner['token'], dm['dm_id'], 0)
    print(dm_messages)

    assert len(dm_messages['messages']) == 1

    assert dm_messages['start'] == 0
    assert dm_messages['end'] == -1

def test_advanced_dm_messages():
    # Test behaviour when 50 messages + 1 more message is sent

    clear_v1()
    owner = auth_register_v2('one@gmail.com', 'pass123', 'one', 'name')
    member = auth_register_v2('two@gmail.com', 'pass123', 'two', 'name')
    dm = dm_create_v1(owner['token'], [member['auth_user_id']])
    messages = message_list(50)
    for message in messages:
        message_senddm_v1(owner['token'], dm['dm_id'], message)

    dm_messages = dm_messages_v1(owner['token'], dm['dm_id'], 0)

    assert len(dm_messages['messages']) == 50
    assert dm_messages['start'] == 0
    assert dm_messages['end'] == -1

    # Send one more message to see if end changed to -1
    message_senddm_v1(owner['token'], dm['dm_id'], 'hello')
    dm_messages = dm_messages_v1(owner['token'], dm['dm_id'], 0)

    assert len(dm_messages['messages']) == 50
    assert dm_messages['start'] == 0
    assert dm_messages['end'] == 50
    assert dm_messages['messages'][0]['message'] == 'hello'

def test_dm_messages_invalid_token():
    '''Test for invalid token'''

    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    non_member1 = auth_register_v2('bake.smith@gmail.com', 'pass123', 'Bake', 'Smith')
    dm = dm_create_v1(owner['token'], [member1['auth_user_id']])
    msgString = 'How are you?'
    message_senddm_v1(owner['token'], dm['dm_id'], msgString)

    with pytest.raises(AccessError):
        dm_messages_v1(0, dm['dm_id'], 0)
    with pytest.raises(AccessError):
        dm_messages_v1({}, dm['dm_id'], 0)
    with pytest.raises(AccessError):
        dm_messages_v1(non_member1['token'], dm['dm_id'], 0)

def test_dm_messages_invalid_dm_id():
    '''Test for invalid dm_id'''

    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    non_member1 = auth_register_v2('bake.smith@gmail.com', 'pass123', 'Bake', 'Smith')
    non_member2 = auth_register_v2('fake.smith@gmail.com', 'pass123', 'Fake', 'Smith')
    dm1 = dm_create_v1(owner['token'], [member1['auth_user_id']])
    dm2 = dm_create_v1(non_member1['token'], [non_member2['auth_user_id']])
    msgString = 'How are you?'
    message_senddm_v1(owner['token'], dm1['dm_id'], msgString)

    with pytest.raises(InputError):
        dm_messages_v1(owner['token'], 0, 0)
    with pytest.raises(InputError):
        dm_messages_v1(owner['token'], str(dm1['dm_id']), 0)
    with pytest.raises(InputError):
        dm_messages_v1(owner['token'], {}, 0)
    with pytest.raises(AccessError):
        dm_messages_v1(owner['token'], dm2['dm_id'], 0)

def test_dm_messages_invalid_start():
    '''Test for invalid start'''

    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    dm = dm_create_v1(owner['token'], [member1['auth_user_id']])

    with pytest.raises(InputError):
        dm_messages_v1(owner['token'], dm['dm_id'], 1)

    msgString = 'How are you?'

    message_senddm_v1(owner['token'], dm['dm_id'], msgString)

    with pytest.raises(InputError):
        dm_messages_v1(owner['token'], dm['dm_id'], 2)

def test_dm_messages_no_messages():
    '''Test for no messages'''
    clear_v1()
    owner = auth_register_v2('john.smith@gmail.com', 'pass123', 'John', 'Smith')
    member1 = auth_register_v2('will.smith@gmail.com', 'pass123', 'Will', 'Smith')
    dm = dm_create_v1(owner['token'], [member1['auth_user_id']])

    assert len(dm_messages_v1(owner['token'], dm['dm_id'], 0)['messages']) == 0

#helper function
@pytest.fixture
def setup():
    clear_v1()

    user_one = auth_register_v2('tunvir@gmail.com', 'tunvir123', 'Tunvir', 'Arora')
    user_two = auth_register_v2('ayaan@gmail.com', 'ayaan1234', 'Ayaan', 'Aadil')
    user_three = auth_register_v2('akshay@gmail.com', 'akshay12345', 'Akshay', 'Verma')

    return[user_one,user_two, user_three]

# dm_create_v1 tests

def test_dm_create_error():
    invalid_id = 123456
    with pytest.raises(AccessError):
        dm_create_v1(invalid_id, [])

    clear_v1()

def test_dm_create_success(setup):
    #create a new dm without third user
    new_dm = dm_create_v1(setup[0]['token'],[setup[1]['auth_user_id']])
    assert new_dm['dm_name'] == 'ayaan.aadil#2,tunvir.arora#1'
    assert new_dm['dm_id'] == 1


    #creating a new dm with just owner
    add_dm = dm_create_v1(setup[0]['token'],[])
    assert add_dm['dm_id'] == 2
    assert add_dm['dm_name'] == 'tunvir.arora#1'

    #creating a new dm with second_user as owner and third user as member
    add_dm1 = dm_create_v1(setup[1]['token'],[setup[2]['auth_user_id']])
    assert add_dm1['dm_id'] == 3
    assert add_dm1['dm_name'] == 'akshay.verma#3,ayaan.aadil#2'

    clear_v1()

# dm_details_v1 tests

def test_dm_details_error(setup):
    token_invalid  = 'invalidToken'
    invalid_id = 1234567

    new_dm = dm_create_v1(setup[0]['token'],[setup[1]['auth_user_id']])

    with pytest.raises(InputError):
        dm_details_v1(setup[0]['token'], invalid_id)
    with pytest.raises(AccessError):
        dm_details_v1(token_invalid, new_dm['dm_id'])

    clear_v1()

def test_dm_details_success(setup):
    new_dm = dm_create_v1(setup[0]['token'],[setup[1]['auth_user_id']])
    dm1 = dm_details_v1(setup[0]['token'], new_dm['dm_id'])
    name = dm1['name']
    members = dm1['members']

    assert name == 'ayaan.aadil#2,tunvir.arora#1'
    assert members[0]['u_id'] == setup[1]['auth_user_id']
    assert members[1]['u_id'] == setup[0]['auth_user_id']

    clear_v1()


# dm_list_v1 tests

#success


def test_dm_list_v1(setup):
    new_dm = dm_create_v1(setup[0]['token'],[setup[1]['auth_user_id']])

    assert dm_list_v1(setup[2]['token']) == {'dms': []}
    assert dm_invite_v1(setup[0]['token'], new_dm['dm_id'], setup[2]['auth_user_id']) == {}

    list1 = dm_list_v1(setup[2]['token'])
    dms1 = list1['dms']

    assert dms1 == [{'dm_id': new_dm['dm_id'], 'name': 'ayaan.aadil#2,tunvir.arora#1'}]
    clear_v1()

#errors

#invalid user_id input for dm_list_v1
def test_invalid_user_list():
    invalid_user_id = 1234567

    with pytest.raises(AccessError):
        dm_list_v1(invalid_user_id)

    clear_v1()

#input is an invalid token for both
def test_invalid_token(setup):
    #create a new dm without third user
    new_dm = dm_create_v1(setup[0]['token'],[setup[1]['auth_user_id']])

    token_invalid = 'invalidToken'
    with pytest.raises(AccessError):
        dm_invite_v1(token_invalid, new_dm['dm_id'], setup[1]['auth_user_id'])

    with pytest.raises(AccessError):
        dm_list_v1(token_invalid)

    clear_v1()

#invalid user inputs

def test_not_verified_invite(setup):
    #create a new dm without third user
    new_dm = dm_create_v1(setup[0]['token'],[setup[1]['auth_user_id']])

    invalid_id = -123456
    with pytest.raises(InputError):
        dm_invite_v1(setup[0]['token'], new_dm['dm_id'], invalid_id)

    #error when the inviting user is not in the dm
    with pytest.raises(AccessError):
        dm_invite_v1(setup[2]['token'], new_dm['dm_id'], setup[2]['auth_user_id'])

    #inviting user who already exists in dm
    with pytest.raises(InputError):
        dm_invite_v1(setup[0]['token'], new_dm['dm_id'], [setup[0]['auth_user_id']])

    clear_v1()

#if dm_id is invalid
def test_dm_invite_error(setup):
    #create a new dm without third user
    dm_create_v1(setup[0]['token'],[setup[1]['auth_user_id']])

    with pytest.raises(InputError):
        dm_invite_v1(setup[0]['token'], -10000, setup[1]['auth_user_id'])

    clear_v1()


#TESTS for dm_remove_v1

#success
def test_dm_remove_success(setup):
    #create a new dm without third user
    new_dm = dm_create_v1(setup[0]['token'],[setup[1]['auth_user_id']])

    assert dm_list_v1(setup[2]['token']) == {'dms': []}
    assert dm_invite_v1(setup[0]['token'], new_dm['dm_id'], setup[2]['auth_user_id']) == {}

    list1 = dm_list_v1(setup[2]['token'])
    dms1 = list1['dms']


    assert dms1 == [{'dm_id': new_dm['dm_id'], 'name': 'ayaan.aadil#2,tunvir.arora#1'}]

    assert dm_remove_v1(setup[0]['token'], new_dm['dm_id']) == {}


    assert dm_list_v1(setup[0]['token']) == {'dms': []}
    assert dm_list_v1(setup[1]['token']) == {'dms': []}

    clear_v1()

#errors
def test_dm_remove_error(setup):
    #create a new dm without third user
    new_dm = dm_create_v1(setup[0]['token'],[setup[1]['auth_user_id']])


    token_invalid = 'invalidToken'
    with pytest.raises(AccessError):
        dm_remove_v1(token_invalid, new_dm['dm_id'])

    #invalid dm_id
    with pytest.raises(InputError):
        dm_remove_v1(setup[0]['token'], -10000)


    with pytest.raises(AccessError):
        dm_remove_v1(setup[1]['token'], new_dm['dm_id'] )

    clear_v1()
