""" Auth functions for iteration 3 """

from src.data import data
import re
from src.error import InputError, AccessError
import jwt
from random import choice, randint 
import secrets 
import smtplib
from email.mime.text import MIMEText


SECRET = 'HEHEXD'
session_number = 0
reset_codes = [] 

def auth_login_v2(email, password):

    ''' 
    This function logs the user in the program given a registered user's email and password
    Arguments:
        email(string)           - Email of the registered user 
        password(string)        - Password of the user 
        
    Exceptions:
        InputError - When email is not valid 
                     Email does not belong to a user 
                     Incorrect password entered 
                     
    Return Value:
        auth_user_id after login is succesfull
    
    
    '''
    

    
    global session_number 
    if check_valid_email(email) == False:
        raise InputError("Invalid email address")

    # Checks if the email is valid or not

    email_found = 0
    for user in data['users']:
        if email == user['email']:
            auth_user_id = user['u_id']
            email_found = 1

    if email_found == 0:
        raise InputError("Email entered does not belong to a user")
        
    session_number += 1
    token =  tokenEncode({'session_id': session_number, 'u_id': auth_user_id})
    
    for user in data['users']:
        if email == user['email'] and password == user['password']:
           
            return ({
                'auth_user_id': user['u_id'],
                'token':  token,
            })

    return InputError ("Email address or password is incorrect")




def auth_register_v2(email, password, name_first, name_last):

   
    ''' 
    Given a user's email, first and last name and password create a new account.
    
    Arguments:
        email(string)           - Email of the registered user 
        password(string)        - Password of the user 
        name_first(string)      - User's first name 
        name_last(string)       - User's last name 
        
    Exceptions:
        InputError - When email is not valid 
                     Email is already registered 
                     Password is less than 6 characters 
                     First and last name has more than 50 characters
                     
    Return Value:
        auth_user_id , token after succesfull registration 
    
    
    '''

    global session_number 

    if check_valid_email(email) == False:
        raise InputError("Invalid email address")

         # Checks if the email is valid or not
    
    session_number += 1
    token = tokenEncode({'session_id': session_number,'u_id': 'auth_user_id'})
    
    for user in data['users']:
        if email == user['email']:
            raise InputError("This email address has already been used")

    if len(password) < 6:
        raise InputError("Password length must be longer than 6 characters")

    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError("First name must be between 1 and 50 characters")

    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError("Last name must be between 1 and 50 characters")
    
    uId = len(data['users']) + 1
    
    handle_str = str(name_first).lower() + '.' + str(name_last).lower()
    id_len = uId + 1
    if len(handle_str) > 20 - id_len:
        handle_str = (handle_str[:18 - id_len] + '..' + '#' + str(uId))
    else:
        handle_str = handle_str + '#' + str(uId)

    
    '''
    handle_str = str(name_first).lower() + str(name_last).lower()
    if len(handle_str) > 20:
        handle_str = handle_str[0:20]
    '''
    # loop through how many of the same handles exist
    
    counter = 0
    for user in data['users']:
        if handle_str in user['handle_str']:
            counter += 1
    if counter != 0:
        handle_str += str(counter - 1)

    # Handle is generated
    
    
    permission_id = 2
    if uId == 1:
        permission_id = 1  # This is the Owner 

    data['users'].append({
        'u_id': uId,
        'email' : email,
        'password':password,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle_str,
        'auth_user_id': uId,
        'token': token,
        'notifications': [],
        'session_list' : [session_number],
        'permission_id': permission_id,
        'channels_num' : 0,
        'dms_num': 0,
        'messages_num': 0,
        'channel_time': 0,
        'dm_time': 0,
        'message_time': 0,
        'profile_img_url': '',
       
        

    })
    
    
    return {
        'auth_user_id': uId,
        'token': token ,
    } 


def auth_logout_v1(token):


    ''' 
    This function takes in token of a user who is already logged in and ends 
    their session
    Arguments:
        token(string) 
   
                     
    Return Value:
        { is_success }
   
    '''


    try: 
        check_token = token_check(token)
        if check_token != {}:
            # remove token from user
            for user in data['users']:
                if user['u_id'] == check_token['u_id']:
                    user['session_list'].remove(check_token['session_id'])
                    return {'is_success': True}
    except:
        return {'is_success': False}
        


def auth_passwordreset_request_v1(email):


    ''' 
    Given a user's email, sends password reset request to the user email 
    
    Arguments:
        email(string)           - Email of the registered user 
       
        
    Exceptions:
        InputError - Email has not been registered 
                     
                     
    Return Value:
        None 
    
    '''

    # check if user is registered 
    
    user_not_found = True
    for user in data['users']:
        if user['email'] == email:
            user_not_found = False
            break

    if user_not_found:
        raise InputError("Email has not been registered")

    # generate a reset code using secrets module 
    reset_code = secrets.token_hex(5)

    user_reset = {
        'email': email,
        'reset_code': reset_code
    }

    reset_code_new = {'reset_code': reset_code}

    # check if user has already requested and if yes, then update
    
    user_requested = False
    for user in reset_codes:
        if user['email'] == email:
            user.update(reset_code_new)
            user_requested = True
            break 

    # append reset_code to the list 
    
    if user_requested == False:
        reset_codes.append(user_reset)

    # send email 
    sender = 'tueaero@gmail.com'
    receiver = [email]

    msg = MIMEText(reset_code)
    msg['Subject'] = 'Reset Code'
    msg['From'] = 'tueaero@gmail.com'
    msg['To'] = email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("tueaero@gmail.com", "Test1531")
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

    return {} 



def auth_passwordreset_reset_v1(reset_code, new_password):

    ''' 
    Given the reset code reset the password and store in the new password  
    
    Arguments:
        reset_code(string)      - reset code to reset the password 
        new_password(string)    - New password which replaces the old password     
       
        
    Exceptions:
        InputError - Reset code is invalid 
                     Length of new password is less than 6 characters  
                     
                     
    Return Value:
        None 
    
    '''
   
    invalid_code = True
    for user in reset_codes:
        
        if reset_code == user.get("reset_code"):
           
            email = user.get("email")
            
            invalid_code = False
            break

    # Raises Input Error for invalid reset code 
    
    if invalid_code == True:
        raise InputError("The reset code is invalid")

    # Raise InputError if password length is less than 6
    
    if len(new_password) < 6:
        raise InputError("Password must be longer than 6 characters")

    
    for user in data['users']:
        if user['email'] == email:
            
            # update the password 
            user.update(new_password)
            break

    return {}




############################ Helper Functions ###################################




reg_ex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
SECRET = 'AERO'
def check_valid_email(email):

    ''' This function checks the validity of the email '''
    if(re.search(reg_ex,email)):
        return True
    else:
        return False
        
    
def tokenEncode(Dict):

    ''' This function encodes the token '''
    global SECRET
    return jwt.encode(Dict, SECRET, algorithm='HS256')
    
def tokenDecode(token):

    ''' This function decodes the token'''
    global SECRET
    if isinstance(token, str) == False:
        raise AccessError
    return jwt.decode(token.encode('ASCII'), SECRET, algorithms=['HS256'])
    
def check_if_login(token, data):
    tokenDict = tokenDecode(token)
    u_id = tokenDict['u_id']
    for user in data['user']:
        if u_id == user['u_id']:
            if user['token'] != None:
                return True
    return False

def token_check(token):

    '''
    This function checks if the token is valid or not
    
    '''

    decode = tokenDecode(token)
    for user in data['users']:
        for session in user['session_list']:
            if session == decode['session_id']:
                return{'u_id' : user['u_id'],'session_id': decode['session_id']}
                


