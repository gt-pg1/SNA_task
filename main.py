import redis
from fastapi import FastAPI

from app.routers import auth, posts, likes

app = FastAPI()

r = redis.Redis(host='localhost', port=6379, db=0)

app.include_router(auth.router, prefix="/api")
app.include_router(posts.router, prefix="/api/posts")
app.include_router(likes.router, prefix="/api/like")
