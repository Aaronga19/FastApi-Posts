from app import schemas
from tests.database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'), "|status:", res.status_code)
    assert res.json().get('message') == 'Welcome to my API - Aaron J.'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={
        'email': "test@test.com",
        'password':'password123',
        'premium': True
        })
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    
    assert new_user.email == 'test@test.com' # res.json().get('email')
    assert res.status_code == 201

def test_login_user(client):
    res = client.post("/login", data={
        'username': "test@test.com",
        'password':'password123'
        })
    print(res.json())
    assert res.status_code==200