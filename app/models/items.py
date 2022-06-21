from typing import List, Optional

import ormar

from app.core.models import AppBaseModel
from app.db.base import BaseMeta


class Category(ormar.Model, AppBaseModel):
    class Meta(BaseMeta):
        tablename = "categories"

    name: str = ormar.String(max_length=100)


class ItemCategory(ormar.Model, AppBaseModel):
    class Meta(BaseMeta):
        tablename = "items_categories"


class Item(ormar.Model, AppBaseModel):
    class Meta(BaseMeta):
        tablename = "items"

    name: str = ormar.String(max_length=128, unique=True, nullable=False)
    price: float = ormar.Float(nullable=False)
    amount: int = ormar.Integer()
    categories: Optional[List[Category]] = ormar.ManyToMany(Category, through=ItemCategory)
