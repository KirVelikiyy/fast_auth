from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas import UserDbSchema, Token
from models import User
from depends import unique_user_params, get_current_active_user, get_db, authenticate_user
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from utils import create_access_token

router = APIRouter()


@router.get('/')
async def index():
    return {'message': 'it is work'}


@router.post("/register/", response_model=UserDbSchema)
async def create_user(
        user: Annotated[User, Depends(unique_user_params)]
):
    new_user_json = UserDbSchema.from_orm(user).json()
    return Response(new_user_json, status_code=status.HTTP_201_CREATED)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


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
