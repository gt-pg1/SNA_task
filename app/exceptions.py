from fastapi import HTTPException


def raise_http_exception(status_code: int, detail: str, headers: dict = None):
    raise HTTPException(
        status_code=status_code,
        detail=detail,
        headers=headers,
    )


def raise_username_already_registered():
    raise_http_exception(400, "Username already registered")


def raise_incorrect_username_or_password():
    raise_http_exception(
        401,
        "Incorrect username or password",
        {"WWW-Authenticate": "Bearer"}
    )


def raise_password_too_short():
    raise_http_exception(400, "The password must be longer than 8 characters.")


def raise_post_not_found():
    raise_http_exception(404, "Post not found")


def raise_not_enough_permissions():
    raise_http_exception(403, "Not enough permissions")


def raise_credentials_exception():
    raise_http_exception(
        401,
        "Token expired or invalid",
        {"WWW-Authenticate": "Bearer"}
    )


def raise_like_own_post():
    raise_http_exception(400, "Can't like own posts")


def raise_already_liked():
    raise_http_exception(400, "Already liked/disliked")


def raise_like_not_found():
    raise_http_exception(404, "Like not found")


def raise_clearbit_exception(e):
    raise_http_exception(400, e)


def raise_invalid_email_hunter():
    raise_http_exception(400, "Invalid email according to emailhunter.co")
