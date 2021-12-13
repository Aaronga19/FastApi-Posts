from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.oauth2 import create_access_token
from app import models
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from alembic import command
from app.config import settings
# from app.settings import secret

# Confidential info 
# host = secret.host
# database = secret.database
# user = secret.user
# password = secret.password

#

#SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:password123@localhost/fastapi_test'

#SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}/{database}_test'    
# For deployig

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'#{settings.database_url}

engine = create_engine(SQLALCHEMY_DATABASE_URL)

print('\nDatabase connection was succesfull for testing!\n')

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
            # run our code after our test finishes

            # Base.metadata.drop_all(bind=engine)
            # command.downgrade("base")

@pytest.fixture
def test_user(client):
    user_data = {'email': 'test@test.com',
        'password':'password123'}
    res = client.post('/users/', json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {'email': 'test123@test.com',
        'password':'password123'}
    res = client.post('/users/', json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client

@pytest.fixture(scope='function')
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user["id"]
    }, {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user["id"]
    }, {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user2["id"]
    }]
    # def create_post_model(post):
    #     return models.Post(**post)
    # post_map= map(create_post_model, posts_data)
    # posts = list(post_map)
    # session.add_all(posts)

    #####

    for post in posts_data:
        session.add_all([models.Post(title=post['title'], content=post['content'], owner_id= post['owner_id'])])
        session.commit()
    print("------------------ SESSION --------------------")
    posts = session.query(models.Post).all()
    return posts