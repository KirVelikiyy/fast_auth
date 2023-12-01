from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.token import TokenData
from schemas.user import UserSchema, CreateUserSchema
from schemas.session import AuthTokensDb
from database.database import get_db
from models.user import User
from models.session import AuthSession
from utils.jwt import TokenManager
from utils.session import create_session_tokens
from exceptions.response import HTTPResponseException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


async def create_user(
        user: CreateUserSchema,
        db: Session = Depends(get_db)
) -> User:
    user_dict: dict = user.dict()
    new_user: User = User(**user_dict)
    try:
        new_user.add_to_db(db)
    except IntegrityError:
        raise HTTPResponseException.user_already_exists()
    return new_user


async def create_auth_session(
        user: User,
        db: Annotated[
            Session, Depends(get_db)
        ]
) -> AuthTokensDb:

    auth_tokens = await create_session_tokens(user.username, user.id)
    new_auth_session = AuthSession(**auth_tokens.dict())

    new_auth_session.add_to_db(db)

    return auth_tokens


async def get_user_by_username(
        username: str,
        db: Annotated[
            Session,
            Depends(get_db)
        ]
) -> User:

    user: User = db.query(User).filter(
        User.username == username
    ).first()

    return user


async def get_current_user(
        access_token: Annotated[
            str,
            Depends(oauth2_scheme)
        ],
        db: Annotated[
            Session,
            Depends(get_db)
        ]
) -> User:
    token_data = TokenManager.decode_token(access_token)
    user = await get_user_by_username(token_data.username, db)
    if user is None:
        raise HTTPResponseException.invalid_credentials()
    return user


async def get_current_active_user(
    current_user: Annotated[
        UserSchema,
        Depends(get_current_user)
    ]
) -> UserSchema:
    if not current_user.is_active:
        raise HTTPResponseException.inactive_user()
    return current_user


async def authenticate_user(
        form_data: Annotated[
            OAuth2PasswordRequestForm,
            Depends()
        ],
        db: Annotated[
            Session,
            Depends(get_db)
        ],
) -> AuthTokensDb:
    user = await get_user_by_username(form_data.username, db)

    if not user or not TokenManager.verify_password(form_data.password, user.hashed_password):
        raise HTTPResponseException.incorrect_username_or_pass()

    auth_tokens = await create_auth_session(user, db)
    return auth_tokens


async def check_refresh_token(
        refresh_token: str,
) -> tuple[TokenData, str]:
    token_data = TokenManager.decode_token(refresh_token)
    return token_data, refresh_token


async def refresh_tokens(
        refresh_token_data: Annotated[
            tuple[TokenData, str],
            Depends(check_refresh_token)
        ],
        db: Annotated[
            Session,
            Depends(get_db)
        ]
) -> AuthTokensDb:
    token_data, refresh_token = refresh_token_data
    username = token_data.username
    user = await get_user_by_username(username, db)
    session: AuthSession | None = db.query(AuthSession).filter(and_(
        AuthSession.user_id == user.id,
        AuthSession.refresh_token == refresh_token
    )).first()

    if not session:
        raise HTTPResponseException.invalid_refresh_token()

    new_auth_tokens = await create_session_tokens(username, user.id)

    session.refresh_token = new_auth_tokens.refresh_token
    session.access_token = new_auth_tokens.access_token

    session.add_to_db(db)

    return new_auth_tokens
