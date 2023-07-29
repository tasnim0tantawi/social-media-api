from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from typing import List
from .. import oauth2


router = APIRouter(
    prefix="/reaction",
    tags=["Reaction"],
    responses={404: {"description": "Not found"}},
)

@router.post("/{id}", status_code=status.HTTP_201_CREATED)
def create_reaction(id: int, reaction: str, db: Session = Depends(get_db),
            current_user:schemas.UserResponse = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    reaction = models.Reaction(post_id=id, user_id=current_user.id, reaction_type=reaction)
    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    return reaction