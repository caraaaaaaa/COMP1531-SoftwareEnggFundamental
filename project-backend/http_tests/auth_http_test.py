"""import pytest
import json
import requests 
from src import config

def test_auth_register_v2():

    #clear
    assert requests.delete(config.url+ 'clear/v1').status_code == 200
        
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': 'nathan1998@gmail.com',
        'password': 'Testingregister123',
        'name_first': 'Nathan',
        'name_last': 'Li',
    })
    assert resp.status_code == 200
    auth_user_id = resp.json()['auth_user_id']
    token = resp.json()['token']
    
    

def test_auth_login_v2():

    
    #clear
    assert requests.delete(config.url+ 'clear/v1').status_code == 200
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        'email': 'nathan1998@gmail.com',
        'password': 'Testingregister123',      
    })
    
    assert resp.status_code == 200
    auth_user_id = resp.json()['auth_user_id']
    token = resp.json()['token']


def test_auth_logout_v1():

    #clear
    assert requests.delete(config.url+ 'clear/v1').status_code == 200
    
    resp = requests.post(config.url + 'auth/logout/v1', json={
        'token' : token ,     
    })
    
    assert resp.status_code == 200
    is_success = resp.json()['is_success : True'] """
    
   

   
