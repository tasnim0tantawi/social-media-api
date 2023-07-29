from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    visibility = Column(String, nullable=False, server_default='public')
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'))
    name = Column(String, nullable=False)


class Reaction(Base):
    __tablename__ = "reactions"
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    reaction_type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'))
    post = relationship("Post")
    user = relationship("User")


