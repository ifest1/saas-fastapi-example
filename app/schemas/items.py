import uuid
from typing import List

from pydantic import BaseModel


class AddCategoryItem(BaseModel):
    item_id: uuid.UUID
    category_id: uuid.UUID


class ItemCategoryOut(BaseModel):
    name: str
    id: uuid.UUID
    

class ItemOut(BaseModel):
    id: uuid.UUID
    name: str
    price: float


class ItemWithCategoriesOut(ItemOut):
    categories: List[ItemCategoryOut]


class CategoryWithItemsOut(ItemCategoryOut):
    items: List[ItemOut]
