def test_register(client, app):
    response = client.post('/api/auth/register', json={
        'name': 'New User',
        'email': 'new@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert 'token' in response.json['data']

def test_register_duplicate_email(client, init_database):
    response = client.post('/api/auth/register', json={
        'name': 'Duplicate User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400

def test_register_short_password(client, app):
    response = client.post('/api/auth/register', json={
        'name': 'Short PW User',
        'email': 'short@example.com',
        'password': '123'
    })
    assert response.status_code == 400

def test_login(client, init_database):
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'token' in response.json['data']
    assert response.json['data']['user']['email'] == 'test@example.com'

def test_login_case_insensitive_and_whitespace(client, init_database):
    response = client.post('/api/auth/login', json={
        'email': '  TEST@Example.com  ',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'token' in response.json['data']

def test_login_invalid_password(client, init_database):
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert 'Invalid credentials' in response.json['message']

def test_login_nonexistent_user(client, init_database):
    response = client.post('/api/auth/login', json={
        'email': 'nobody@example.com',
        'password': 'password123'
    })
    assert response.status_code == 401

def test_auth_me(client, init_database):
    login_res = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = login_res.json['data']['token']
    
    me_res = client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})
    assert me_res.status_code == 200
    assert me_res.json['data']['email'] == 'test@example.com'

def test_auth_me_unauthorized(client):
    me_res = client.get('/api/auth/me')
    assert me_res.status_code == 401
