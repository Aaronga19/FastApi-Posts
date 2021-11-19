#from app.main import *
from fastapi import status, HTTPException, Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app import oauth2
from .. import models, schemas
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# API

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int= 0, search: Optional[str]= ""):
    # SQL 
    """cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()"""
    # ORM
    print(f"Request by '{current_user.id}' - {current_user.email}")
    # to filter by user _ posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # SQL
    '''cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()'''
    
    # LISTS
    """post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)"""

    # ORM
    
    print(f"Request by '{current_user.id}' - {current_user.email}")
    new_post = models.Post(owner_id=current_user.id,**post.dict()) # Post(**Post.dict()) instead of Post(title=post.title, content=post.content... so on) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    
# title str, content str
@router.get("/latest")
def get_latest_post():
    return {"Message": "This url doesn't work yet"}
    """post = my_posts[len(my_posts)-1]
    return post"""

@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # SQL CODE
    '''cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()'''

    # ORM 
    post = db.query(models.Post).filter(models.Post.id==id).first()
    #post = find_post(id)
    if post != None:
        return post

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
        
 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """deleting post"""


    # SQL CODE
    '''cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    post = cursor.fetchone()
    conn.commit()'''

    # ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()

    #post = post_query

    #find the index in the array that has required id 
    
    #index =  find_index_post(id)
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    else:
        db.delete(post)
        db.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post {id} deleted succesfully!")


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, api_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.update(api_post.dict(), synchronize_session=False)
    #post_query.update({"title":f"{post.title}","content":f"{post.content}"}, synchronize_session=False)
    db.commit()


    #LISTS
    """post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict"""

    
    return post_query.first()