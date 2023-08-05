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

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_reaction(id: int, reaction: schemas.Reaction, db: Session = Depends(get_db),
            current_user:schemas.UserResponse = Depends(oauth2.get_current_user)):
    
    reaction_query = db.query(models.Reaction).filter(models.Reaction.post_id == reaction.post_id, models.Reaction.user_id == current_user.id)
    reaction = reaction_query.first()
    if(reaction.direction == 1):
        if reaction:
            # User already reacted to this post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already reacted to this post.")
        
        new_reaction = models.Reaction(post_id=reaction.post_id, user_id=current_user.id, reaction_type=reaction.reaction_type, direction=reaction.direction)
        db.add(new_reaction)
        db.commit()
        db.refresh(new_reaction)
        return {"message": "Reaction created successfully."}
    else:
        if not reaction: 
            # User did not react to this post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You did not react to this post to unlike it.")
        
        db.delete(reaction)
        db.commit()
        return {"message": "Reaction deleted successfully."}