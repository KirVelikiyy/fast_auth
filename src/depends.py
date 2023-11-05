from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import jwt

from schemas import UserSchema, TokenData, CreateUserSchema
from database import get_db
from models import User
from config import SECRET_KEY, ALGORITHM
from utils import get_password_hash, verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def unique_user_params(user: CreateUserSchema, db: Session = Depends(get_db)) -> User:
    user_dict: dict = user.dict()

    password = user_dict.pop('password')
    hashed_password = get_password_hash(password)
    user_dict.update({"hashed_password": hashed_password})

    new_user = User(**user_dict)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with that e-mail or username already exists'
        )
    return new_user


async def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> User:
    user: User = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user_id parameter'
        )
    return user


async def get_user_by_username(username: str, db: Annotated[Session, Depends(get_db)]) -> User:
    user: User = db.query(User).filter(User.username == username).first()
    return user


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = await get_user_by_username(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def authenticate_user(username: str, password: str, db):
    user = await get_user_by_username(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

