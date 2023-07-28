from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from .secret import key
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer



# Secret key for signing JWT token
# Hashing algorithm
# Expiration time

SECRET_KEY = key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        

        token_data = schemas.TokenData(user_id=user_id)

    except JWTError:
        raise credentials_exception

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return verify_access_token(token, credentials_exception)
