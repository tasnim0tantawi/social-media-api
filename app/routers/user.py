from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import get_db
from typing import List


router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user( user:schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash_password(user.password)
    user = models.User(username=user.username, password=hashed_password, email=user.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

