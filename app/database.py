from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from psycopg2.extras import RealDictCursor
import json
import psycopg2
import time
# con variables de entorno
# from config import settings
# host = settings.database_hostname #so on



# Confidential info DEVELOPING
# from app.settings import secret
# host = secret.host
# database = secret.database
# user = secret.user
# password = secret.password

# SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}/{database}'

# CONFIDENTIAL INFO DEPLOYING 
from app.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'#{settings.database_url}


#{settings.database_url}
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

# Conect database without ORM - SQL only

# def connect_database(host, database, user, password):
#     while True:

#         try:
#             conn = psycopg2.connect(host=host, database=database, user=user, password=password, cursor_factory=RealDictCursor)
#             cursor = conn.cursor()
#             #print("Tipo:",type(cursor))
#             #print('\nDatabase connection was succesfull!\n')
#             break
#         except Exception as error:
#             print('Connecting to database failed')
#             print('Error: ', error)
#             time.sleep(2)

# Database connection SQL vanilla
# host = get_secret('host')
# database = get_secret('database')
# user = get_secret('user')
# password = get_secret('password')


# connect_database(host, database ,user, password)

# # To fix

# conn = psycopg2.connect(host=host, database=database, user=user, password=password, cursor_factory=RealDictCursor)
# cursor = conn.cursor()

# request Get method url: "/"