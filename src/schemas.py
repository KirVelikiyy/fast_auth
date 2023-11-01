from datetime import datetime
from pydantic import BaseModel


class ProductSchema(BaseModel):
    title: str
    price: int


class ProductDbSchema(ProductSchema):
    product_id: int


class UserSchema(BaseModel):
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = False
    hashed_password: str


class UserDbSchema(UserSchema):
    user_id: int
    added_at: datetime
