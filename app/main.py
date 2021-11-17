from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# Schemas

# For Json
import json

# Databases
from app import models, schemas
from app.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

# Web server
import uvicorn


app = FastAPI()
models.Base.metadata.create_all(bind=engine)





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

# API

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # SQL 
    """cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()"""
    # ORM
    posts = db.query(models.Post).all()

    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # SQL
    '''cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()'''
    
    # LISTS
    """post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)"""

    # ORM
    new_post = models.Post(**post.dict()) # Post(**Post.dict()) instead of Post(title=post.title, content=post.content... so on) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    
# title str, content str
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return post

@app.get("/posts/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    
    # SQL CODE
    '''cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()'''

    # ORM 
    post = db.query(models.Post).filter(models.Post.id==id).first()
    #post = find_post(id)
    if post != None:
        return post
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
        
 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    """deleting post"""


    # SQL CODE
    '''cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    post = cursor.fetchone()
    conn.commit()'''

    # ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()

    #find the index in the array that has required id 
    
    #index =  find_index_post(id)
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    else:
        db.delete(post)
        db.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post {id} deleted succesfully!")


@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, api_post: schemas.PostCreate, db: Session = Depends(get_db)):
    """ Updating post"""

    # SQL CODE
    '''cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",(post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()'''
    
    # ORM
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    """index =  find_index_post(id)"""

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")

    post_query.update(api_post.dict(), synchronize_session=False)
    #post_query.update({"title":f"{post.title}","content":f"{post.content}"}, synchronize_session=False)
    db.commit()


    #LISTS
    """post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict"""

    
    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # ORM
    new_user = models.User(**user.dict()) # Post(**Post.dict()) instead of Post(title=post.title, content=post.content... so on) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"User Created": new_user}


if __name__=='__main__':
    uvicorn.run(app)


