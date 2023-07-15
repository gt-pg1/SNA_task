from fastapi import HTTPException, status


def raise_username_already_registered():
    raise HTTPException(status_code=400, detail="Username already registered")


def raise_incorrect_username_or_password():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def raise_post_not_found():
    raise HTTPException(status_code=404, detail="Post not found")


def raise_not_enough_permissions():
    raise HTTPException(status_code=403, detail="Not enough permissions")


def raise_credentials_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired or invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )


def raise_like_own_post():
    raise HTTPException(status_code=400, detail="Can't like own posts")


def raise_already_liked():
    raise HTTPException(status_code=400, detail="Already liked/disliked")


def raise_like_not_found():
    raise HTTPException(status_code=404, detail="Like not found")