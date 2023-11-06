from typing import Annotated
from fastapi import APIRouter, Depends, Response, status

from schemas.user import UserDbSchema
from schemas.token import TokenResponse
from models import User
from depends import unique_user_params, get_current_active_user, authenticate_user
from utils.jwt import TokenManager
from exceptions.response import HTTPResponseException

router = APIRouter()


@router.post("/register/", response_model=UserDbSchema)
async def create_user(
        user: Annotated[User, Depends(unique_user_params)]
):
    new_user_json = UserDbSchema.from_orm(user).json()
    return Response(new_user_json, status_code=status.HTTP_201_CREATED)


@router.post("/login/", response_model=TokenResponse)
async def login_for_access_token(
    user: Annotated[User, Depends(authenticate_user)]
):
    if not user:
        raise HTTPResponseException.incorrect_username_or_pass()

    access_token = TokenManager.create_access_token(
        data={
            "sub": user.username
        }
    )
    refresh_token = TokenManager.create_refresh_token(
        data={
            "sub": user.username,
            "access_token": access_token,
        }
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


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
