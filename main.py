from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel  # To validate the 
from random import randrange

import uvicorn
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published : bool = True # Default value
    rating: Optional[int] = None 

my_posts = [
    {"id": 1, "title": "title of post 1", "content": "content of post 1"}, 
    {"id": 2, "title": "favourite food", "content": "I like pechuguita"}
    ]

# Functions

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# request Get method url: "/"

@app.get("/")
async def get_user():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# title str, content str
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):

    post = find_post(id)
    if post != None:
        return {"data": f"Here is post {post}"}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id {id} does not exist"}



if __name__=='__main__':
    uvicorn.run(app)