from jose import JWTError, jwt

# Secret key for signing JWT token
# Hashing algorithm
# Expiration time

SECRET_KEY = "b2e7e4e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30