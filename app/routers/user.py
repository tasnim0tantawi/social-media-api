from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import get_db

# We use the APIRouter class to create a router, and then we can add our paths to it with the decorator syntax.
router = APIRouter(
    prefix="/users", # Prefix for the path, so we don't have to write /users/ in every path
    tags=["Users"], # Tags are for documentation purposes
    responses={404: {"description": "Not found"}}, # Custom error message
)

# Schema is used to define the structure of the data sent to the API 
# To validate the data sent bu the user, we use Pydantic's BaseModel class.
# This way we make sure that the data sent by the user is in the correct format and is what we expect.
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user( user:schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash_password(user.password)
    user = models.User(password=hashed_password, email=user.email, name = user.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# We use pydantic's BaseModel class to define the structure of the data received from the API so we make sure we only send the data we want to send.
# We use the orm_mode = True to tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
# Ths assures that we don't send the password hash to the user or any other data we don't want to send or expose or the user doesn't need to know.
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    # first() returns the first result of the query without continuing to searching until the end of the users table. Once we find the first result, we stop searching.
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

