from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel  # To validate the 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# For Json
import json

# Databases
from app import models
from app.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

# Web server
import uvicorn


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class Post(BaseModel):
    title: str
    content: str
    published : bool = True # Default value
    #rating: Optional[int] = None 



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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "Success"}

# API

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    return {"data": new_post}

# title str, content str
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/posts/{id}")
async def get_post(id: str, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    #post = find_post(id)
    if post != None:
        return {"post_detail": post}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id {id} does not exist"}
 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """deleting post"""

    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    #find the index in the array that has required id 
    
    #index =  find_index_post(id)

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post deleted {id} succesfully!")


@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, post:Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",(post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    #index =  find_index_post(id)

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    conn.commit()
    return {'data': updated_post}


if __name__=='__main__':
    uvicorn.run(app)


