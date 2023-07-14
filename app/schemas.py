from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class LikeBase(BaseModel):
    user_id: int
    post_id: int
    value: int


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
