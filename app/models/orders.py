from typing import List, Optional

import ormar

from app.core.models import AppBaseModel
from app.db.base import BaseMeta


class Order(ormar.Model, AppBaseModel):
    class Meta(BaseMeta):
        tablename = "orders"

    # name: str = ormar.String(max_length=128, unique=True, nullable=False)
    # state =
    # amount: int = ormar.Integer()
    # categories: Optional[List[Item]] = ormar.ManyToMany(Item, through=ItemCategory)
