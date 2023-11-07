from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_HOURS
from schemas.token import TokenData
from exceptions.response import HTTPResponseException


pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])


class TokenGenerator:
    @classmethod
    def create_token(cls, expires_delta: timedelta, **kwargs) -> str:
        to_encode = kwargs.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_access_token(cls, expire_minutes: int | None = None, **kwargs) -> str:
        """

        :param expire_minutes:
        :param kwargs: sub (subject) - username
        """
        expires_delta = timedelta(minutes=expire_minutes or ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = cls.create_token(expires_delta, **kwargs)
        return access_token

    @classmethod
    def create_refresh_token(cls, expire_hours: int | None = None, **kwargs) -> str:
        """

        :param expire_hours:
        :param kwargs: sub (subject) - username
        """
        expires_delta = timedelta(hours=expire_hours or REFRESH_TOKEN_EXPIRE_HOURS)
        refresh_token = cls.create_token(expires_delta, **kwargs)
        return refresh_token


class TokenManager(TokenGenerator):
    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        return pwd_context.hash(password)

    @staticmethod
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
