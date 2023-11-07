from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.user import UserSchema, CreateUserSchema
from schemas.session import AuthTokensDb, AuthTokens
from database.database import get_db
from models.user import User
from models.session import AuthSession
from utils.jwt import TokenManager
from exceptions.response import HTTPResponseException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


async def create_user(
        user: CreateUserSchema,
        db: Session = Depends(get_db)
) -> User:
    user_dict: dict = user.dict()
    new_user: User = User(**user_dict)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPResponseException.user_exists()
    return new_user


async def create_auth_session(user: User, db: Annotated[Session, Depends(get_db)]) -> AuthTokensDb:
    access_token = TokenManager.create_access_token(sub=user.username)
    refresh_token = TokenManager.create_refresh_token(sub=user.username)

    auth_tokens = AuthTokensDb(user_id=user.id, access_token=access_token, refresh_token=refresh_token)
    new_auth_session = AuthSession(**auth_tokens.dict())

    db.add(new_auth_session)
    db.commit()
    db.refresh(new_auth_session)

    return auth_tokens


async def get_user_by_username(
        username: str,
        db: Annotated[Session, Depends(get_db)]
) -> User:
    user: User = db.query(User).filter(User.username == username).first()
    return user


async def get_current_user(
        access_token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)]
) -> User:
    token_data = TokenManager.decode_token(access_token)
    user = await get_user_by_username(token_data.username, db)
    if user is None:
        raise HTTPResponseException.invalid_credentials()
    return user


async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)]
) -> UserSchema:
    if not current_user.is_active:
        raise HTTPResponseException.inactive_user()
    return current_user


async def authenticate_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[Session, Depends(get_db)],
) -> bool | AuthTokensDb:
    user = await get_user_by_username(form_data.username, db)
    if not user:
        return False
    if not TokenManager.verify_password(form_data.password, user.hashed_password):
        return False

    auth_tokens = await create_auth_session(user, db)
    return auth_tokens
