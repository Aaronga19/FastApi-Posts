from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

with open("secret.json") as f:
    secret = json.loads(f.read())

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "la variable %s no existe" % secret_name
        raise (msg)

host = get_secret('host')
database = get_secret('database')
user = get_secret('user')
password = get_secret('password')

SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

print('\nDatabase connection was succesfull!\n')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()