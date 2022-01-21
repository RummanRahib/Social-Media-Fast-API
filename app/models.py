from sqlalchemy import (TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        String, text)
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
  __tablename__ = "posts"
  
  id = Column(Integer, primary_key=True, nullable=False)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  published = Column(Boolean, server_default='TRUE', nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
  # foreign key userId pointing to the id of users table
  userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  user = relationship("User")
  

class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Like(Base):
  __tablename__ = "likes"
  userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  postId = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
