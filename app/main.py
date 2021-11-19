

from fastapi import FastAPI

from app import database

from .routers import post, user, auth

# Databases
from app import models
from app.database import engine
# Web server
import uvicorn



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# ROUTERS
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def get_user():
    return {"message": "Welcome to my API"}

if __name__=='__main__':
    uvicorn.run(app)

