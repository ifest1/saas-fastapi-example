from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.models.categories import Category

router = APIRouter()


@router.post("/", response_model=Category, status_code=201)
async def create_category(category: Category):
    await category.save()
    if not category:
        raise HTTPException(status_code=404, detail="Couldn't create category.")
    return category


@router.get("/{id}/", response_model=Category)
async def read_category(
    id: int = Path(..., gt=0),
):
    category = await Category.objects.get(pk=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    return category


@router.get("/", response_model=List[Category])
async def read_all_categories():
    return await Category.objects.all()


@router.put("/{id}/", response_model=Category)
async def update_category(category_id: int, category: Category):
    category_db = await Category.objects.get(pk=category_id)
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found.")
    return await category_db.update(**category.dict())


@router.delete("/{id}/", response_model=Category)
async def delete_category(id: int, category: Category = None):
    if category:
        return {"deleted_rows": await category.delete()}

    category_db = await Category.objects.get(pk=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")

    return {"deleted_rows": await category_db.delete()}
