from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from .secret import key

# Secret key for signing JWT token
# Hashing algorithm
# Expiration time

SECRET_KEY = key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithms=ALGORITHM)
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

def get_current_user():
    pass