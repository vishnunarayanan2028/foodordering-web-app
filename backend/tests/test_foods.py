def test_get_foods(client):
    response = client.get('/api/foods/')
    assert response.status_code == 200
