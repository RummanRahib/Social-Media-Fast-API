from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas

router = APIRouter(
  prefix="/like",
  tags=['Like']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(database.get_db), userID: int =Depends(oauth2.getCurrentUser)):
  
  # if post exists
  post = db.query(models.Post).filter(models.Post.id == like.postId).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"Post with id {like.postId} does not exist")
  
  #  if like exits
  
  likeQuery = db.query(models.Like).filter(models.Like.postId == like.postId, models.Like.userId == userID.id)
  foundLike = likeQuery.first()
  
  if(like.direction == 1):
    if foundLike:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                          detail=f"{userID.id} has already voted on post {like.postId}")
    
    newLike = models.Like(postId = like.postId, userId = userID.id)
    db.add(newLike)
    db.commit()
    return {
      "message": "successfully liked"
    }
    
  else:
    if not foundLike:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"Like does not exist")
      
    likeQuery.delete(synchronize_session=False)
    db.commit()
    
    return {
      "message": "successfully removed like"
    }
