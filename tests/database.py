from fastapi.testclient import TestClient
import pytest

from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from alembic import command
from app.settings import secret

# Confidential info 
host = secret.host
database = secret.database
user = secret.user
password = secret.password

#

#SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:password123@localhost/fastapi_test'

SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}/{database}_test'    #{settings.database_url}


engine = create_engine(SQLALCHEMY_DATABASE_URL)

print('\nDatabase connection was succesfull for testing!\n')

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope='module')
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope='module')
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