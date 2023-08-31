from typing import Literal

from pydantic import BaseModel, validator, ValidationError


class Product(BaseModel):
    name: str
    price: int
    sku: str


class Cart(BaseModel):
    products: list[Product] = []


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    role: Literal['stuff', 'client', 'admin'] = 'client'
    cart: Cart = Cart()

    @validator('first_name', 'last_name')
    def name_length(cls, v, field):
        if len(v) > 16:
            raise ValueError(f"{field.name} is too long (>16)")
        return v.title()


class Users(BaseModel):
    users: list[User]
