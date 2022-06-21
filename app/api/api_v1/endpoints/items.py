from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from ormar import NoMatch

from app.core.auth import oauth2_scheme
from app.models.items import Category, Item
from app.schemas.items import AddCategoryItem, ItemWithCategoriesOut

router = APIRouter()


@router.post("/", response_model=ItemWithCategoriesOut, status_code=201)
# async def create_item(item: Item, token: str = Depends(oauth2_scheme)):
async def create_item(item: Item):
    item = await item.save()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't create item.",
        )
    return item


@router.post("/add_category", response_model=ItemWithCategoriesOut, status_code=201)
async def add_item_category(item_category: AddCategoryItem, token: str = Depends(oauth2_scheme)):
    try:
        item = await Item.objects.get(pk=item_category.item_id)
        category = await Category.objects.get(pk=item_category.category_id)
    except NoMatch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item/category not found.",
        )
    await item.categories.add(category)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't add category to item..",
        )

    return item


@router.get("/{id}/", response_model=ItemWithCategoriesOut, status_code=200)
async def read_item(
    id: int = Path(..., gt=0),
):
    item = await Item.objects.get(pk=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item not found.")
    return item


@router.get("/", response_model=List[ItemWithCategoriesOut])
async def read_all_items():
    return await Item.objects.select_related("categories").all()


@router.put("/{id}/", response_model=ItemWithCategoriesOut)
async def update_item(item_id: int, item: Item, token: str = Depends(oauth2_scheme)):
    item_db = await Item.objects.get(pk=item_id)
    if not item_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item not found.")
    return await item_db.update(**item.dict())


@router.delete("/{id}/", response_model=ItemWithCategoriesOut)
async def delete_item(id: int, item: Item = None, token: str = Depends(oauth2_scheme)):
    if item:
        return {"deleted_rows": await item.delete()}

    item_db = await Item.objects.get(pk=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item not found.")

    return {"deleted_rows": await item_db.delete()}
