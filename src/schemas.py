from pydantic import BaseModel


class ProductSchema(BaseModel):
    title: str
    price: int


class ProductDbSchema(ProductSchema):
    product_id: int
