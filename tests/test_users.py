import pytest

def test_add_user(client, fake_user):
    response = client.post('/add_user', json=fake_user)
    
    assert response.status_code == 200
    
    data = response.json()

    assert 'success' in data
    assert 'message' in data

def test_get_users(client):
    response = client.get('/users?limit=1&page=1')

    assert response.status_code == 200
    assert response.json()['success'] == True