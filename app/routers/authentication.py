from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from .. import oauth2, utils


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid user email or password")
    
    if not utils.verify_password(user_credentials.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid user email or password")
    
    # Create access JWT token for user if the user is valid

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

