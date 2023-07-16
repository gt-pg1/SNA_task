from typing import Dict, Any

from fastapi import Depends, APIRouter

from sqlalchemy.orm import Session

from app import exceptions, database, crud, schemas, dependencies

router = APIRouter()

DETAIL_MESSAGES = {
    -1: {"detail": "Post disliked"},
    1: {"detail": "Post liked"},
    "deleted": {"detail": "Like deleted"}
}


@router.post("/{post_id}", response_model=Dict[str, Any])
def add_like(
        post_id: int,
        like: schemas.LikeCreate,
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user)
) -> Dict[str, Any]:
    post = crud.get_post(db, post_id)

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
        if existing_like['value'] != like.value:
            if existing_like['from_redis']:
                print('to redis')
                crud.save_redis_like(post_id, current_user.id, like.value)
            else:
                existing_like['value'] = like.value
                db.commit()
            return DETAIL_MESSAGES.get(like.value)

        exceptions.raise_already_liked()

    like = schemas.LikeBase(post_id=post_id, value=like.value)
    crud.create_like(db=db, like=like, user_id=current_user.id)
    crud.save_redis_like(post_id, current_user.id, like.value)
    return DETAIL_MESSAGES.get(like.value)


@router.delete("/{post_id}", response_model=Dict[str, Any])
def remove_like(
        post_id: int,
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user)
) -> Dict[str, Any]:
    like = crud.get_like_by_user_and_post(
        db,
        user_id=current_user.id,
        post_id=post_id
    )

    if not like:
        exceptions.raise_like_not_found()

    crud.delete_like(db=db, post_id=post_id, user_id=current_user.id)

    like = crud.get_like_by_user_and_post(
        db,
        user_id=current_user.id,
        post_id=post_id
    )

    if not like or like['from_redis']:
        return DETAIL_MESSAGES.get("deleted")
    else:
        exceptions.raise_like_not_found()
