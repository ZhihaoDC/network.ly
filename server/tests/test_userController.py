import json
from src.services import UserService
from src.models.UserModel import User
def test_signup(client):
    """
        GIVEN the user is not authenticated
        WHEN the user tries to sign up and api receives POST request in endpoint '/create-user' 
        THEN register the new user in database
    """
    #this user does not exist in the database
    data_mock = {
        'username': 'test_user_12345',
        'email': 'test_user_12345@gmail.com',
        'password': 'secur3p4ssword'
    }

    response = client.post('/create-user',
                           json=data_mock)
    response_json = response.get_json()

    user_exists = UserService.get_by_email(User, email=data_mock['email'])
    
    assert response.status_code == 200
    assert 'jwt' in response_json
    assert 'password' not in response_json
    assert user_exists


def test_signup_existing_user(client):

    #this user has been previously added
    data_mock = {
        'username': 'test_user_12345',
        'email': 'test_user_12345@gmail.com',
        'password': 'secur3p4ssword'
    }
    
    response = client.post('/create-user',
                           json=data_mock)
    
    assert response.status_code == 409 #already exists
    assert 'password' not in response.get_json().keys()


def test_login(client):
    data_mock = {
        'identification': 'test_user_12345',
        'password': 'secur3p4ssword'
    }

    response = client.post('/login',
                           json=data_mock)
    
    response_json = response.get_json()
    assert response.status_code == 200
    assert 'jwt' in response_json
    assert 'password' not in response_json
    assert response_json['user']['username'] == data_mock['identification']


def test_login_wrong_password(client):
    data_mock = {
        'identification': 'test_user_12345',
        'password': 'wr0ngp4ssword'
    }

    response = client.post('/login',
                           json=data_mock)
    response_json = response.get_json()
    assert response.status_code == 401
    assert 'jwt' not in response_json
    