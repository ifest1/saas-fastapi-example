from typing import Optional

import ormar

from app.db.base import BaseMeta
from app.models.categories import Category


class Item(ormar.Model):
    class Meta(BaseMeta):
        tablename = "items"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=128, unique=True, nullable=False)
    price: float = ormar.Float(default=True, nullable=False)
    category: Optional[Category] = ormar.ForeignKey(Category, nullable=True)
