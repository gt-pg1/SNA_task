from typing import List, Dict
from fastapi import Depends, APIRouter

from sqlalchemy.orm import Session

from app import crud, models, schemas, database, dependencies, exceptions

router = APIRouter()


def get_post_by_id(db: Session, post_id: int):
    """
    Get a specific post by ID from the database.

    Args:
        db (Session): The database session to use.
        post_id (int): The ID of the post to retrieve.

    Returns:
        Post: The retrieved Post object.

    Raises:
        PostNotFoundException: If the post with the specified ID is not found.
    """
    post = crud.get_post(db, post_id)
    if not post:
        exceptions.raise_post_not_found()
    return post


@router.get("/{post_id}", response_model=schemas.Post)
def read_post(
        *,
        db: Session = Depends(database.get_db),
        post_id: int,
        current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    Get a specific post by ID.
    Returns the post if found.
    """
    post = get_post_by_id(db, post_id)
    return post


@router.get("/", response_model=List[schemas.Post])
def read_posts(
        *,
        db: Session = Depends(database.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    Get multiple posts.
    Returns a list of posts.
    """
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@router.post("/", response_model=schemas.Post)
def create_post(
        *,
        db: Session = Depends(database.get_db),
        post_in: schemas.PostCreate,
        current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    Create a new post.
    Returns the created post.
    """
    post = crud.create_post(
        db=db,
        post=post_in,
        user_id=current_user.id
    )
    return post


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(
        *,
        db: Session = Depends(database.get_db),
        post_id: int, post_in: schemas.PostCreate,
        current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    Update an existing post by ID.
    Returns the updated post.
    """
    post = get_post_by_id(db, post_id)
    if not post:
        exceptions.raise_post_not_found()
    if post.user_id != current_user.id:
        exceptions.raise_not_enough_permissions()
    post = crud.update_post(db=db, post_id=post_id, post_in=post_in)
    return post


@router.delete("/{post_id}", response_model=schemas.PostDelete)
def delete_post(
        *,
        db: Session = Depends(database.get_db),
        post_id: int,
        current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    Delete a post by ID.
    Returns a message indicating the deletion status.
    """
    post = get_post_by_id(db, post_id)
    if post.user_id != current_user.id:
        exceptions.raise_not_enough_permissions()
    crud.delete_post(db=db, post_id=post_id)

    detail = schemas.PostDelete(
        detail="The post has been successfully deleted"
    )

    return detail


@router.get("/likes/{post_id}", response_model=Dict[str, List[int]])
def get_likes(
        post_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    Get the likes and dislikes for a specific post.
    Returns a dictionary with 'likes' and 'dislikes' keys,
    each containing a list of user IDs.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        exceptions.raise_post_not_found()

    likes = crud.get_likes(db, post_id)

    like_user_ids = [
        like['user_id'] for like in likes if like['value'] == 1
    ]
    dislike_user_ids = [
        like['user_id'] for like in likes if like['value'] == -1
    ]

    return {
        "likes": like_user_ids,
        "dislikes": dislike_user_ids
    }
