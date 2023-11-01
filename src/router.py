from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import ProductSchema, ProductDbSchema, UserSchema, UserDbSchema
from database import get_db
from models import Product, User

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
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    user_dict = user.dict()
    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response = {**user_dict, "user_id": new_user.user_id, "added_at": new_user.added_at}
    return response
