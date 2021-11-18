from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .routers import post, user, auth
# Schemas

# For Json
import json

# Databases
from app import models, schemas, utils
from app.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

# Web server
import uvicorn


app = FastAPI()



models.Base.metadata.create_all(bind=engine)

# ROUTERS
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# charge json
with open("secret.json") as f:
    secret = json.loads(f.read())

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "la variable %s no existe" % secret_name
        raise (msg)


# Global var
        
my_posts = [
    {"id": 1, "title": "title of post 1", "content": "content of post 1"}, 
    {"id": 2, "title": "favourite food", "content": "I like pechuguita"} 
    ]

# Functions

def connect_database(host, database, user, password):
    while True:

        try:
            conn = psycopg2.connect(host=host, database=database, user=user, password=password, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            #print("Tipo:",type(cursor))
            #print('\nDatabase connection was succesfull!\n')
            break
        except Exception as error:
            print('Connecting to database failed')
            print('Error: ', error)
            time.sleep(2)

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# Database connection SQL PURE
host = get_secret('host')
database = get_secret('database')
user = get_secret('user')
password = get_secret('password')


connect_database(host, database ,user, password)

# To fix

conn = psycopg2.connect(host=host, database=database, user=user, password=password, cursor_factory=RealDictCursor)
cursor = conn.cursor()

# request Get method url: "/"

@app.get("/")
async def get_user():
    return {"message": "Welcome to my API"}






if __name__=='__main__':
    uvicorn.run(app)


