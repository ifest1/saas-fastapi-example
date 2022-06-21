import uuid

from app.core.cache import CartsCache
from app.models.items import Item


class CartService(object):
    @staticmethod
    async def add_item(cart_id: str, item_id: uuid.UUID):
        item = await Item.objects.get(pk=item_id)
        if not CartsCache.is_cart_created(cart_id):
            CartsCache.create_empty_cart(cart_id)

        CartsCache.add_cart_item(cart_id, item)
        return item

    @staticmethod
    def list_items(cart_id: str):
        if not CartsCache.is_cart_created(cart_id):
            return CartsCache.create_empty_cart(cart_id)

        return CartsCache.list_cart_items(cart_id)

    @staticmethod
    def delete_item(cart_id: str, item_id: str):
        if not CartsCache.is_cart_created(cart_id):
            CartsCache.create_empty_cart(cart_id)
            return []
        return CartsCache.remove_cart_item(cart_id, str(item_id))

    @staticmethod
    def decrease_item(cart_id: str, item_id: str):
        pass
