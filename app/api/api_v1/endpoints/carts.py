import uuid
from typing import List

from fastapi import APIRouter, Request, status

from app.models.items import Item
from app.schemas.carts import Cart
from app.services.carts import CartService

router = APIRouter()


@router.get("/", response_model=Cart, status_code=status.HTTP_200_OK)
async def list_cart_items(request: Request):
    cart_id = request.session.get("session_data").get("cart_id")
    return CartService.list_items(cart_id)


@router.post("/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def add_cart_item(item_id: uuid.UUID, request: Request):
    cart_id = request.session.get("session_data").get("cart_id")
    return await CartService.add_item(cart_id, item_id)


@router.delete(
    "/{item_id}", response_model=List[Item], status_code=status.HTTP_200_OK
)
async def remove_cart_item(item_id: uuid.UUID, request: Request):
    cart_id = request.session.get("session_data").get("cart_id")
    return CartService.delete_item(cart_id, item_id)


@router.post(
    "/decrease/{item_id}", response_model=Cart, status_code=status.HTTP_200_OK
)
async def decrease_item_amount(item_id: uuid.UUID, request: Request):
    pass


@router.post(
    "/increase/{item_id}", response_model=Cart, status_code=status.HTTP_200_OK
)
async def increase_item_amount(item_id: uuid.UUID, request: Request):
    pass
