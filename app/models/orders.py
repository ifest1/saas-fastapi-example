import uuid
from enum import Enum
from typing import List

import ormar

from app.core.models import AppBaseModel
from app.db.base import BaseMeta
from app.models.items import Item
from app.models.users import User


class PaymentMethod(Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    PIX = "PIX"


class OrderState(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"


class Payment(ormar.Model, AppBaseModel):
    class Meta(BaseMeta):
        tablename = "payments"

    method: str = ormar.String(max_length=100, choices=list(PaymentMethod))


class OrderItem(ormar.Model, AppBaseModel):
    class Meta(BaseMeta):
        tablename = "orders_items"


class Order(ormar.Model, AppBaseModel):
    class Meta(BaseMeta):
        tablename = "orders"

    state: str = ormar.String(max_length=100, choices=list(OrderState))
    payment: int = ormar.ForeignKey(Payment, nullable=True)
    user_id: uuid.UUID = ormar.ForeignKey(User)
    total: int = ormar.Integer()
    items: List[Item] = ormar.ManyToMany(Item, through=OrderItem)
