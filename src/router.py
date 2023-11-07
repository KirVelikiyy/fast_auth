from typing import Annotated
from fastapi import APIRouter, Depends, Response, status

from schemas.user import UserDbSchema
from schemas.session import AuthTokens, AuthTokensDb
from models.user import User
from depends import create_user, get_current_active_user, authenticate_user
from exceptions.response import HTTPResponseException


router = APIRouter()


@router.post("/register/", response_model=UserDbSchema)
async def register(
        user: Annotated[User, Depends(create_user)]
):
    new_user_json = UserDbSchema.from_orm(user).json()
    return Response(new_user_json, status_code=status.HTTP_201_CREATED)


@router.post("/login/", response_model=AuthTokens)
async def login(
    auth_tokens_db: Annotated[AuthTokensDb, Depends(authenticate_user)]
):
    if not auth_tokens_db:
        raise HTTPResponseException.incorrect_username_or_pass()
    auth_tokens_json = AuthTokens(**auth_tokens_db.dict()).json()
    return Response(auth_tokens_json, status_code=status.HTTP_201_CREATED)


@router.get("/users/me/", response_model=UserDbSchema)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    user_json = UserDbSchema.from_orm(current_user).json()
    return Response(user_json, status_code=status.HTTP_200_OK)


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
