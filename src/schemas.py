from datetime import datetime
from pydantic import BaseModel, EmailStr


class ProductSchema(BaseModel):
    title: str
    price: int


class ProductDbSchema(ProductSchema):
    product_id: int


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = True
    is_admin: bool | None = False
    hashed_password: str


class UserDbSchema(UserSchema):
    user_id: int
    added_at: datetime

    class Config:
        orm_mode = True
