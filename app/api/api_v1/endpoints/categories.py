from uuid import UUID
from typing import List
from ormar import NoMatch

from fastapi import APIRouter, HTTPException, Path, status

from app.models.items import Category
from app.schemas.items import CategoryWithItemsOut

router = APIRouter()


@router.post("/", response_model=CategoryWithItemsOut, status_code=201)
async def create_category(category: Category):
    await category.save()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't create category.",
        )
    return category


@router.get("/{id}/", response_model=CategoryWithItemsOut)
async def read_category(
    id: int = Path(..., gt=0),
):
    category = await Category.objects.get(pk=id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found.",
        )
    return category


@router.get("/", response_model=List[CategoryWithItemsOut])
async def read_all_categories():
    return await Category.objects.select_related("items").all()


@router.put("/{id}/", response_model=CategoryWithItemsOut)
async def update_category(category_id: int, category: Category):
    category_db = await Category.objects.get(pk=category_id)
    if not category_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found.",
        )
    return await category_db.update(**category.dict())


@router.delete("/{id}/", status_code=204)
async def delete_category(id: UUID):
    try:
        category_db = await Category.objects.get(pk=id)
    except NoMatch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found.",
        )

    await category_db.delete()

    return None
