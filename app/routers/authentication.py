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
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid user email or password")
    
    if not user.verify_password(user_credentials.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid user email or password")
    
    # Create access JWT token for user if the user is valid


    return {"message": "Login"}
