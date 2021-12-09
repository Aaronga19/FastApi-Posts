

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import database

from .routers import post, user, auth, vote

# Databases
from app import models
from app.database import engine
# Web server
import uvicorn



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
#models.Base.metadata.create_all(bind=engine)

# ROUTERS
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def get_user():
    return {"message": "Welcome to my API - Aaron J."}

if __name__=='__main__':
    uvicorn.run(app)

