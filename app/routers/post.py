from sys import prefix
from typing import List, Optional

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
  prefix="/posts",
  tags=['Posts']
)

# GET ALL POSTS STARTS

@router.get("/", response_model=List[schemas.ResponseModelWithLike])
def getPosts(db: Session = Depends(get_db), userID: int =Depends(oauth2.getCurrentUser), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
  # Usual SQL query method
  # cursor.execute(''' SELECT * FROM posts ''')
  # posts = cursor.fetchall()
  
  # SQLAlchemy ORM method
  # posts = db.query(models.Post).all()
  
  # posts with query params
  # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  # posts with like info
  posts = db.query(models.Post, func.count(models.Like.postId).label("likes")).join(models.Like, models.Like.postId == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  
  return posts

# GET ALL POSTS ENDS


# CREATE POST STARTS

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseModel)
def createPosts(post: schemas.CreatePost, db: Session = Depends(get_db), userID: int =Depends(oauth2.getCurrentUser)):
  # Usual SQL query method
  # cursor.execute(''' INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''', (post.title, post.content, post.published))
  # newPost = cursor.fetchone()
  # conn.commit() # must to save in DB
  
  # print(userID)
  
  # SQLAlchemy ORM method
  # newPost = models.Post(title=post.title, content=post.content, published=post.published)
  newPost = models.Post(userId = userID.id, **post.dict())
  db.add(newPost)
  db.commit()
  db.refresh(newPost)
  return newPost

# CREATE POST ENDS


# GET POST BY ID STARTS

@router.get("/{id}", response_model=schemas.ResponseModelWithLike)
def getPost(id: int, db: Session = Depends(get_db), userID: int =Depends(oauth2.getCurrentUser)):
  # Usual SQL query method
  # cursor.execute(''' SELECT * from posts WHERE id = %s ''', (str(id),))
  # post = cursor.fetchone()
  
  # SQLAlchemy ORM method
  # post = db.query(models.Post).filter(models.Post.id == id).first()
  # ppst with like info
  post = db.query(models.Post, func.count(models.Like.postId).label("likes")).join(models.Like, models.Like.postId == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
  if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with {id} not found")
  return post

# GET POST BY ID ENDS


# DELETE POST BY ID STARTS


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletPost(id: int, db: Session = Depends(get_db), userID: int = Depends(oauth2.getCurrentUser)):
  # Usual SQL query method
  # cursor.execute(''' DELETE FROM posts WHERE id = %s RETURNING * ''', (str(id),))
  # deletedPost = cursor.fetchone()
  # conn.commit()
  
  # SQLAlchemy ORM method
  deletedPostQuery = db.query(models.Post).filter(models.Post.id == id)
  post = deletedPostQuery.first()
  # print(post.userId, userID.id, type(post.userId), type(userID.id))
  
  if post == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with {id} does not exist")
  
  # logic for Update only own posts
  if post.userId != int(userID.id):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail=f"Not authorized to perform the action")
  deletedPostQuery.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

# DELETE POST BY ID ENDS


# UPDATE POST BY ID STARTS

@router.put("/{id}", response_model=schemas.ResponseModel)
def updatePost(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), userID: int =Depends(oauth2.getCurrentUser)):
  # Usual SQL query method
  # cursor.execute(''' UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * ''', (post.title, post.content, post.published, str(id),))
  # updatedPost = cursor.fetchone()
  # conn.commit()
  
  # SQLAlchemy ORM method
  updatedPost = db.query(models.Post).filter(models.Post.id == id)
  if updatedPost.first() == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with {id} does not exist")
  
  # logic for Update only own posts
  if updatedPost.first().userId != int(userID.id):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail=f"Not authorized to perform the action")
  updatedPost.update(post.dict(), synchronize_session=False)
  db.commit()
  return updatedPost.first()
    
# UPDATE POST BY ID ENDS
