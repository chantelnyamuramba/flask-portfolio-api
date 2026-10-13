def test_health_check(client):
    """Test the GET /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_user_registration(client):
    """Test POST /api/auth/register with valid user data."""
    payload = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Password123!'
    }
    response = client.post('/api/auth/register', json=payload)
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'
    assert response.json['user']['username'] == 'testuser'


def test_user_login(client):
    """Test user registration followed by a POST /api/auth/login."""
    # 1. Register a user
    client.post('/api/auth/register', json={
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'Password123!'
    })

    # 2. Login with credentials
    response = client.post('/api/auth/login', json={
        'username': 'loginuser',
        'password': 'Password123!'
    })

    assert response.status_code == 200
    assert 'access_token' in response.json