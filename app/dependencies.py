from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from . import crud, schemas, database, security, exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)
):
    token_data = None
    try:
        payload = jwt.decode(
            token,
            security.SECRET_KEY,
            algorithms=[security.ALGORITHM]
        )
        username: str = payload.get("username")
        if username is None:
            exceptions.raise_credentials_exception()

        token_data = schemas.TokenData(username=username)
    except JWTError:
        exceptions.raise_credentials_exception()

    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        exceptions.raise_credentials_exception()

    return user
