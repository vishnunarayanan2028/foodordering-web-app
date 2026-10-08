def test_customer_cannot_access_admin(client, init_database):
    login_resp = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = login_resp.json['data']['token']
    
    response = client.get('/api/admin/dashboard', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403
