from sqlalchemy.orm import Session

from . import models, schemas, security


def get_user_by_username(db: Session, username: str):
    user = db.query(
        models.User
    ).filter(
        models.User.username == username
    ).first()
    return user


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=security.get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    verify_password = security.verify_password(password, user.hashed_password)
    if not user or not verify_password:
        raise ValueError("Invalid username or password")
    return user


def get_post(db: Session, post_id: int):
    post = db.query(
        models.Post
    ).filter(
        models.Post.id == post_id
    ).first()
    return post


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    posts = db.query(
        models.Post
    ).offset(
        skip
    ).limit(
        limit
    ).all()
    return posts


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.model_dump(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post is not None:
        db.delete(db_post)
        db.commit()
        return True
    return False


def update_post(db: Session, post_id: int, post_in: schemas.PostCreate):
    db_post = get_post(db, post_id)
    if db_post is None:
        return False
    post_data = {
        var: value
        for var, value in vars(post_in).items()
        if value is not None
    }

    db.query(
        models.Post
    ).filter(
        models.Post.id == post_id
    ).update(post_data)

    db.commit()
    return db_post


def get_like(db: Session, like_id: int):
    like = db.query(
        models.Like
    ).filter(
        models.Like.id == like_id
    ).first()
    return like


def get_like_by_user_and_post(db: Session, user_id: int, post_id: int):
    like = db.query(
        models.Like
    ).filter(
        models.Like.user_id == user_id,
        models.Like.post_id == post_id
    ).first()
    return like


def create_like(db: Session, like: schemas.LikeCreate, user_id: int):
    db_like = models.Like(**like.model_dump(), user_id=user_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def delete_like(db: Session, like_id: int):
    like = get_like(db, like_id)
    db.delete(like)
    db.commit()
    return {"detail": "Like deleted"}
