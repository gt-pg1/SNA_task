from sqlalchemy.orm import Session

from app import models, schemas, security, clearbit
import main


def get_user_by_username(db: Session, username: str):
    """
    Fetches a user by the username from the database.

    Args:
        db (Session): The database session to use.
        username (str): The username of the user.

    Returns:
        User: The User object if found.
    """
    user = db.query(
        models.User
    ).filter(
        models.User.username == username
    ).first()
    return user


def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user in the database and
    fetches additional user data from Clearbit.

    Args:
        db (Session): The database session to use.
        user (schemas.UserCreate): The user data.

    Returns:
        User: The newly created User object.
    """
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=security.get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    clearbit.get_clearbit_data(user.email)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticates a user by username and password.

    Args:
        db (Session): The database session to use.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        User: The authenticated User object.

    Raises:
        ValueError: If the authentication fails.
    """
    user = get_user_by_username(db, username)
    verify_password = security.verify_password(password, user.hashed_password)
    if not user or not verify_password:
        raise ValueError("Invalid username or password")
    return user


def get_post(db: Session, post_id: int):
    """
    Retrieves a post by its ID from the database.

    Args:
        db (Session): The database session to use.
        post_id (int): The ID of the post.

    Returns:
        Post: The Post object if found.
    """
    post = db.query(
        models.Post
    ).filter(
        models.Post.id == post_id
    ).first()
    return post


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of posts from the database.

    Args:
        db (Session): The database session to use.
        skip (int, optional): Number of posts to skip. Defaults to 0.
        limit (int, optional): Maximum number of posts to return. Defaults to 100.

    Returns:
        List[Post]: List of Post objects.
    """
    posts = db.query(
        models.Post
    ).offset(
        skip
    ).limit(
        limit
    ).all()
    return posts


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    """
    Creates a new post in the database.

    Args:
        db (Session): The database session to use.
        post (schemas.PostCreate): The post data.
        user_id (int): The ID of the user who is creating the post.

    Returns:
        Post: The newly created Post object.
    """
    db_post = models.Post(**post.model_dump(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    """
    Deletes a post by its ID from the database.

    Args:
        db (Session): The database session to use.
        post_id (int): The ID of the post.

    Returns:
        bool: True if the post was deleted, False otherwise.
    """
    db_post = get_post(db, post_id)
    if db_post is not None:
        db.delete(db_post)
        db.commit()
        return True
    return False


def update_post(db: Session, post_id: int, post_in: schemas.PostCreate):
    """
    Updates a post by its ID in the database.

    Args:
        db (Session): The database session to use.
        post_id (int): The ID of the post.
        post_in (schemas.PostCreate): The new post data.

    Returns:
        Post: The updated Post object.
    """
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


def get_likes(db: Session, post_id: int):
    """
    Retrieves likes for a post by its ID from the database.

    Args:
        db (Session): The database session to use.
        post_id (int): The ID of the post.

    Returns:
        List[Like]: List of Like objects.
    """
    key = f"post:{post_id}:likes"
    likes_from_redis = main.r.hgetall(key)

    if likes_from_redis:
        likes = [
            {
                'user_id': int(user_id.decode().split(':')[1]),
                'value': int(value.decode())
            }
            for user_id, value in likes_from_redis.items()
        ]
    else:
        likes_db = db.query(
            models.Like
        ).filter(
            models.Like.post_id == post_id
        ).all()

        likes = [
            {
                'user_id': like.user_id,
                'value': like.value
            } for like in likes_db
        ]

        for like in likes_db:
            save_redis_like(post_id, like.user_id, like.value)
    return likes


def get_like_by_user_and_post(db: Session, user_id: int, post_id: int):
    """
    Retrieves a like by user and post IDs from the database.

    Args:
        db (Session): The database session to use.
        user_id (int): The ID of the user.
        post_id (int): The ID of the post.

    Returns:
        dict: Dictionary containing like data.
    """
    like_value = get_redis_like(post_id, user_id)

    if like_value is not None:
        return {'like_id': None, 'value': like_value, 'from_redis': True}

    like = db.query(
        models.Like
    ).filter(
        models.Like.user_id == user_id,
        models.Like.post_id == post_id
    ).first()

    if like is None:
        return None

    return {'like_id': like.id, 'value': like.value, 'from_redis': False}


def create_like(db: Session, like: schemas.LikeCreate, user_id: int):
    """
    Creates a new like in the database.

    Args:
        db (Session): The database session to use.
        like (schemas.LikeCreate): The like data.
        user_id (int): The ID of the user who is creating the like.

    Returns:
        Like: The newly created Like object.
    """
    db_like = models.Like(**like.model_dump(), user_id=user_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def delete_like(db: Session, post_id: int, user_id: int):
    """
    Deletes a like by user and post IDs from the database.

    Args:
        db (Session): The database session to use.
        post_id (int): The ID of the post.
        user_id (int): The ID of the user.

    Returns:
        dict: Dictionary containing the result message.
    """
    like = db.query(
        models.Like
    ).filter(
        models.Like.user_id == user_id,
        models.Like.post_id == post_id
    ).first()

    if like is None:
        return None

    db.delete(like)
    db.commit()
    remove_redis_like(post_id, user_id)
    return {"detail": "Like deleted"}


def get_redis_like(post_id: int, user_id: int):
    """
    Retrieves a like by user and post IDs from the Redis cache.

    Args:
        post_id (int): The ID of the post.
        user_id (int): The ID of the user.

    Returns:
        int: The like value if found, else None.
    """
    key = f"post:{post_id}:likes"
    field = f"user:{user_id}"
    value = main.r.hget(key, field)
    return int(value) if value is not None else None


def save_redis_like(post_id: int, user_id: int, value: int):
    """
    Saves a like by user and post IDs to the Redis cache.

    Args:
        post_id (int): The ID of the post.
        user_id (int): The ID of the user.
        value (int): The like value.
    """
    key = f"post:{post_id}:likes"
    field = f"user:{user_id}"
    main.r.hset(key, field, value)


def remove_redis_like(post_id: int, user_id: int):
    """
    Removes a like by user and post IDs from the Redis cache.

    Args:
        post_id (int): The ID of the post.
        user_id (int): The ID of the user.
    """
    key = f"post:{post_id}:likes"
    field = f"user:{user_id}"
    main.r.hdel(key, field)
    if not main.r.hkeys(key):
        main.r.delete(key)
