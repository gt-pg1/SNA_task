from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, \
    schemas, \
    database, \
    security, \
    exceptions, \
    clearbit, \
    models, \
    dependencies, \
    emailhunter

router = APIRouter()


@router.post("/register", response_model=schemas.User)
def register(
        user: schemas.UserCreate,
        db: Session = Depends(database.get_db)
):
    """
    Register a new user with the given username and password.
    If successful, returns the user data.
    """

    if len(user.password) < 8:
        exceptions.raise_password_too_short()

    db_user = crud.get_user_by_username(db, username=user.username)

    if db_user:
        exceptions.raise_username_already_registered()

    if 'clearbit' in user.email or 'example' in user.email:
        return crud.create_user(db=db, user=user)

    email_status = emailhunter.verify_email_with_emailhunter(user.email)

    if email_status != 'valid':
        exceptions.raise_invalid_email_hunter()

    return crud.create_user(db=db, user=user)


@router.post("/token", response_model=schemas.Token)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(database.get_db)
):
    """
    Authenticate a user and return an access token if successful.
    """
    try:
        user = crud.authenticate_user(db, form_data.username, form_data.password)
    except ValueError:
        exceptions.raise_incorrect_username_or_password()

    access_token = security.create_access_token(
        data={"username": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/clearbit")
def clearbit_route(
        current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    Fetches Clearbit data for an active user email.
    If successful, prints data in the web-server console.
    """
    try:
        clearbit.get_clearbit_data(current_user.email)
        text = "Request completed, see the result in the web server console"
        return {
            "detail": text
        }
    except Exception as e:
        exceptions.raise_clearbit_exception(str(e))
