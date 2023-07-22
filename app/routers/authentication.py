from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from ... import schemas, models
from ..database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
def login(db: Session = Depends(get_db)):
    return {"message": "Login"}
