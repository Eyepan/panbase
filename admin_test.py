import requests
from app import app
from database import db


def test_login_admin():
    # Test a successful login
    response = requests.post('http://localhost:8000/api/admin/login', data={
        'username': 'admin',
        'password': 'admin'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'

    # Test an invalid username
    response = requests.post('http://localhost:8000/api/admin/login', data={
        'username': 'invalid_username',
        'password': 'admin'
    })
    assert response.status_code == 400
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Invalid username'

    # Test an invalid password
    response = requests.post('http://localhost:8000/api/admin/login', data={
        'username': 'admin',
        'password': 'invalid_password'
    })
    assert response.status_code == 400
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Invalid password'


def test_register_admin():
    response = requests.post(
        'http://localhost:8000/api/admin/register', json={
            'username': 'test_user',
            'password': 'test_password'
        })
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'

    # Test a duplicate username
    response = requests.post('http://localhost:8000/api/admin/register', json={
        'username': 'admin',
        'password': 'test_password'
    })
    assert response.status_code == 400
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Username already exists'


def test_who_am_i():
    # Test with valid admin token
    token = requests.post('http://localhost:8000/api/admin/login', data={
        'username': 'admin',
        'password': 'admin'
    }).json()['access_token']
    response = requests.get(
        'http://localhost:8000/api/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'username' in response.json()
    assert response.json()['username'] == 'admin'

    # Test with invalid token
    response = requests.get(
        'http://localhost:8000/api/me', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 400
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Invalid token'

    # Test with valid user token
    db.run_query(
        "INSERT INTO admins (username, password) VALUES (:username, :password)",
        username="test_user", password=db.encrypt("test_password")
    )

    response = requests.post('http://localhost:8000/token', data={
        'username': 'test_user',
        'password': 'test_password'
    })

    token = response.json()['access_token']
    response = requests.get(
        'http://localhost:8000/api/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'username' in response.json()
    assert response


test_who_am_i()
