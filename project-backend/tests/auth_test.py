# Tests for auth functions 


import pytest
import src.auth as auth
from src.channel import *
from src.auth import auth_logout_v1
from src.other import clear_v1
from src.error import InputError, AccessError


##########################################################################
#                                                                        #
#                     auth_register_v2 testing functions                 #
#                                                                        #
##########################################################################

def test_auth_register_v2():
    clear_v1()

    #user = auth.auth_register_v2('nathan1998@gmail.com', 'Testingregister123' , 'Nathan' , 'Li')
    


    '''result = auth.auth_register_v1('iheartunsw@gmail.com', 'LoveUNSW123' , 'Unsw' , 'Sydney')
    assert result == {'auth_user_id' : 2}
    #auth.auth_login_v1('iheartunsw@gmail.com', 'LoveUNSW123')''' 


#    #Successful register and login

def test_auth_register_InputError():   

    clear_v1()

    with pytest.raises(InputError):
        auth.auth_register_v2('tennis.com','ilovetennis','Tennis','Sport')

    # Email entered is not a valid email

    auth.auth_register_v2('iheartunsw@gmail.com','ilovetennis','Tennis','Sport')
    with pytest.raises(InputError):
        auth.auth_register_v2('iheartunsw@gmail.com','ilovetennis','Tennis','Sport')

    # Email address is already being used by another user

    with pytest.raises(InputError):
        auth.auth_register_v2('nathan@gmail.com','love','Nathan','Arora')

    # Password entered is less than 6 characters long

    with pytest.raises(InputError):
        auth.auth_register_v2('tunvir@gmail.com','squash123','qwertyuiopasdfghjkllzxcvbnmmmmqwertyuiopasdfghjklllllllllllllll','Arora')

    # First name is not between 1 and 50 characters


    with pytest.raises(InputError):
        auth.auth_register_v2('tunvir@gmail.com','squash123','Arora','qwertyuiopasdfghjkllzxcvbnmmmmqwertyuiopasdfghjklllllllllllllll')

    # Last name is not between 1 and 50 characters
    

##########################################################################
#                                                                        #
#                     auth_login_v2 testing functions                    #
#                                                                        #
##########################################################################

def test_auth_login_v2():

    clear_v1()
    auth.auth_register_v2('nathan1998@gmail.com', 'Testingregister123', 'Nathan', 'Li')

    assert auth.auth_login_v2('nathan1998@gmail.com', 'Testingregister123')
   

def test_auth_login_inputError():
    clear_v1()

   
    with pytest.raises(InputError):
        auth.auth_login_v2('tunvir1@gmail.com','squash123')

    # Email entered does not belong to a user

   
    with pytest.raises(InputError):
        auth.auth_login_v2('tunvir1@gmail.com','testing')

    # Password is not correct
    
    
    
##########################################################################
#                                                                        #
#                     auth_logout_v1 testing functions                   #
#                                                                        #
##########################################################################  


def test_logout_v1():
    #test successful logout
    
    user = auth.auth_register_v2('nathan1998@gmail.com', 'Testingregister123' , 'Nathan' , 'Li')
    assert auth.auth_login_v2('nathan1998@gmail.com', 'Testingregister123')
    assert auth_logout_v1(user['token']) == {'is_success': True}
    clear_v1()

def test_logout_v1_unsuccessful():
    #test unsuccessful logout
    invalid_token = 12345
    
    assert auth_logout_v1(invalid_token) == {'is_success': False}
    clear_v1()

"""def test_auth_passwordreset_reset_InputError():
    '''
    Test the inputerrors for password reset
    '''

    clear_v1()

    result = auth.auth_register_v2('bob@gmail.com', 'ilovemeatballs', 'bob', 'builder')
    token = result['token']

    auth.auth_logout_v1(token)

    auth.auth_passwordreset_request_v1('bob@gmail.com')

    with pytest.raises(InputError):
        auth.auth_passwordreset_reset_v1('notcorrectlol', 'iforgotmypassword') """

##########################################################################
#                                                                        #
#                     auth_password_reset_request_v1 testing             #
#                                                                        #
##########################################################################

def test_unregistered_user():
    clear_v1()
    with pytest.raises(InputError):
        auth.auth_passwordreset_request_v1("unregistereduser@gmail.com")
        

"""def test_auth_passwordreset_request():
        
    user = auth.auth_register_v2('tueaero@gmail.com', 'Test1531' , 'Nathan' , 'Li')
    auth.auth_passwordreset_request_v1('tueaero@gmail.com')
    code = auth.reset_codes[0].get('reset_code')
    auth.auth_passwordreset_reset_v1(code, 'new_password')
    auth.auth_logout_v1(user_1.get("token"))
    auth.auth_login_v2('tueaero@gmail.com', 'new_password') """


##########################################################################
#                                                                        #
#                     auth_passwordreset_reset_v1 testing                #
#                                                                        #
##########################################################################
  
def test_invalid_resetcode():
    clear_v1()
    auth.auth_register_v2("tueaero@gmail.com", "password", "Nathan", "Li")
    invalid_code = 123213
    with pytest.raises(InputError):
        auth.auth_passwordreset_reset_v1(invalid_code, "newpassword")
        
        
"""def test_password_invalid():
    clear_v1()
    auth.auth_register_v2("tueaero@gmail.com", "password", "Nathan", "Li")
    auth.auth_passwordreset_request_v1("tueaero@gmail.com")
    code = auth.reset_codes[0].get('reset_code')
    with pytest.raises(InputError):
        auth.auth_passwordreset_reset_v1(code, "wrong")
"""
