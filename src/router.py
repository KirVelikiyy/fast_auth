from typing import Annotated
from fastapi import APIRouter, Depends, Response, status

from schemas import UserDbSchema
from models import User
from depends import user_doesnt_exists, correct_user_id

router = APIRouter()


@router.get('/')
async def index():
    return {'message': 'it is work'}


@router.post("/register/", response_model=UserDbSchema)
async def create_user(
        user: Annotated[User, Depends(user_doesnt_exists)]
):
    new_user_json = UserDbSchema.from_orm(user).json()
    return Response(new_user_json, status_code=status.HTTP_201_CREATED)


@router.get("/users/{user_id}", response_model=UserDbSchema)
async def get_user(user: Annotated[User, Depends(correct_user_id)]):
    user_json = UserDbSchema.from_orm(user).json()
    return Response(user_json, status_code=status.HTTP_200_OK)
