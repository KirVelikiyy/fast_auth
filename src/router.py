from typing import Annotated
from fastapi import APIRouter, Depends, Response, status

from schemas.user import UserDbSchema
from schemas.session import AuthTokens, AuthTokensDb
from models.user import User
from depends import create_user, get_current_active_user, authenticate_user, refresh_tokens


router = APIRouter()


@router.post("/register/", response_model=UserDbSchema)
async def register(
        user: Annotated[User, Depends(create_user)]
):
    new_user_json = UserDbSchema.from_orm(user).json()
    return Response(new_user_json, status_code=status.HTTP_201_CREATED)


@router.post("/login/")
async def login(
    auth_tokens_db: Annotated[AuthTokensDb, Depends(authenticate_user)]
):
    auth_tokens_dict = AuthTokens(**auth_tokens_db.dict()).dict()

    return auth_tokens_dict


@router.post("/refresh/")
async def refresh_token(
        auth_tokens_db: Annotated[AuthTokensDb, Depends(refresh_tokens)]
):
    auth_tokens_dict = AuthTokens(**auth_tokens_db.dict()).dict()

    return auth_tokens_dict


@router.get("/users/me/", response_model=UserDbSchema)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    user_json = UserDbSchema.from_orm(current_user).json()
    return Response(user_json, status_code=status.HTTP_200_OK)
