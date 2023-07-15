from fastapi import FastAPI

from app.routers import auth, posts, likes

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(posts.router, prefix="/api/posts")
app.include_router(likes.router, prefix="/api/like")
