import json

from redis import Redis

from app.core.config import settings
from app.models.items import Item

cache = Redis(
    host=settings.CACHE_HOST,
    port=settings.CACHE_PORT,
    password=settings.CACHE_PASSWORD,
    db=0,
)


"""
Redis user's cart schema:
[
    "cart_id": {
        "total_price": "float",
        "items": [
            {
                "id": "int",
                "amount": "int",
                "name": "str",
                "price": "float"
            }
        ]
    }
]
"""


class CartsCache(object):
    @staticmethod
    def _get_carts():
        carts = cache.get("carts")
        if carts:
            return json.loads(carts)
        return {}

    def _get_cart_items(carts, cart_id: str):
        return carts.get(cart_id).get("items")

    @staticmethod
    def create_empty_cart(cart_id: str):
        empty_cart = {cart_id: {"total_price": 0.0, "items": []}}
        data = json.dumps(empty_cart)
        cache.set("carts", data)
        return empty_cart

    @staticmethod
    def list_cart_items(cart_id: str):
        carts = CartsCache._get_carts()
        user_cart = carts.get(cart_id)
        user_cart.update({"cart_id": cart_id})
        return user_cart

    @staticmethod
    def is_cart_created(cart_id: str):
        carts = CartsCache._get_carts()

        if not carts:
            return False

        if cart_id in carts:
            return True

        return False

    @staticmethod
    def get_cart(cart_id: str):
        carts = CartsCache._get_carts()
        return carts.get(cart_id)

    @staticmethod
    def add_cart_item(cart_id: str, item: Item):
        user_cart = CartsCache._get_carts().get(cart_id)
        cart_items = user_cart.get("items")

        item_is_already_included = False

        if cart_items:
            for index, cart_item in enumerate(cart_items):
                if cart_item.get("id") == str(item.id):
                    cart_items[index].update(
                        {"amount": cart_item.get("amount") + 1}
                    )
                    item_is_already_included = True

        if not item_is_already_included:
            cart_items.append(
                {
                    "id": str(item.id),
                    "amount": 1,
                    "name": item.name,
                    "price": item.price,
                }
            )

        current_total_price = user_cart.get("total_price")
        user_cart.update(
            {
                "items": cart_items,
                "total_price": current_total_price + item.price,
            }
        )
        data = json.dumps({cart_id: user_cart})
        cache.set("carts", data)

    @staticmethod
    def remove_cart_item(cart_id: str, item_id: str):
        user_cart = CartsCache._get_carts().get(cart_id)
        cart_items = user_cart.get("items")
        new_items = []

        for index, cart_item in enumerate(cart_items):
            if cart_item.get("id") != item_id:
                new_items.append(cart_item)

        item_price = cart_items[index].get("price")
        item_amount = cart_items[index].get("amount")
        current_total_price = user_cart.get("total_price")
        user_cart.update(
            {
                "items": new_items,
                "total_price": current_total_price - (item_price * item_amount),
            }
        )
        data = json.dumps({cart_id: user_cart})
        cache.set("carts", data)
        return new_items

    @staticmethod
    def decrease_cart_item_amount(cart_id: str, item_id: int):
        user_cart = CartsCache._get_carts().get(cart_id)
        cart_items = user_cart.get("items")

        updated_item = None

        for index, item in enumerate(cart_items):
            if item.get("id") == item_id:
                updated_item = item

        if not updated_item:
            return

        updated_item.update({"amount": updated_item.get("amount") - 1})
        cart_items[index] = updated_item
        current_total_price = user_cart.get("total_price")
        user_cart.update(
            {
                "items": cart_items,
                "total_price": current_total_price - updated_item.get("price"),
            }
        )
        data = json.dumps({cart_id: user_cart})
        cache.set("carts", data)
