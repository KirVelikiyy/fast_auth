from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

from config import SECRET_KEY, ALGORITHM
from schemas.token import TokenData
from exceptions.response import HTTPResponseException


pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPResponseException.invalid_credentials()
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise HTTPResponseException.invalid_credentials()
    return token_data
