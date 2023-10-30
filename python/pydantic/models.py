import datetime
from typing import Literal

from pydantic import BaseModel, validator, Field


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
    registration_date: Field(default_factory=datetime.date.today())
    last_seen_date: datetime.date = None

    @validator('first_name', 'last_name')
    def name_length(cls, v, field):
        if len(v) > 16:
            raise ValueError(f"{field.name} is too long (>16)")
        return v.title()


class Users(BaseModel):
    users: list[User]
