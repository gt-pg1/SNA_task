from typing import Dict, List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .. import exceptions, database, crud, schemas, dependencies

router = APIRouter()


@router.post("/{post_id}")
def add_like(
        post_id: int,
        like: schemas.LikeCreate,
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user)
):
    post = crud.get_post(db, post_id)
    detail_disliked = {"detail": "Post disliked"}
    detail_liked = {"detail": "Post liked"}

    if not post:
        exceptions.raise_post_not_found()

    if post.user_id == current_user.id:
        exceptions.raise_like_own_post()

    existing_like = crud.get_like_by_user_and_post(
        db=db,
        user_id=current_user.id,
        post_id=post_id
    )

    if existing_like:
        if existing_like.value == like.value:
            exceptions.raise_already_liked()
        else:
            existing_like.value = like.value
            db.commit()
            return detail_disliked if like.value == -1 else detail_liked

    like = schemas.LikeBase(post_id=post_id, value=like.value)
    crud.create_like(db=db, like=like, user_id=current_user.id)
    return detail_liked if like.value == 1 else detail_disliked


@router.delete("/{post_id}")
def remove_like(
        post_id: int,
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user)
):
    like = crud.get_like_by_user_and_post(
        db,
        user_id=current_user.id,
        post_id=post_id
    )
    detail_deleted = {"detail": "Like deleted"}

    if not like:
        exceptions.raise_like_not_found()
    crud.delete_like(db=db, like_id=like.id)
    return detail_deleted
