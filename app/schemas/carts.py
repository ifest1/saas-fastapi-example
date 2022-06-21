from typing import List

from pydantic import BaseModel


class CartItem(BaseModel):
    id: str
    price: str
    amount: str


class Cart(BaseModel):
    cart_id: str
    total_price: float
    items: List[CartItem] = []
