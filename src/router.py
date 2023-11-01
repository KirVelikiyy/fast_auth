from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from schemas import ProductSchema, ProductDbSchema, UserDbSchema
from database import get_db
from models import Product, User
from depends import user_doesnt_exists, correct_user_id

router = APIRouter()


@router.get('/')
async def index():
    return {'message': 'it is work'}


@router.post("/products/", response_model=ProductDbSchema)
async def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    product_dict = product.dict()
    new_product = Product(**product_dict)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    response = {**product_dict, "product_id": new_product.product_id}
    return response


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
