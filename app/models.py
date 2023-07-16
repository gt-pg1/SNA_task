from sqlalchemy import Column, \
    Integer, \
    String, \
    Text, \
    ForeignKey, \
    CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    posts = relationship('Post', backref='user', cascade='all,delete')


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    likes = relationship('Like', backref='post', cascade='all,delete')


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'))
    value = Column(Integer, CheckConstraint('value=-1 OR value=1'), nullable=False)

