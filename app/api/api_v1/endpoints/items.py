from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.models.items import Item

router = APIRouter()


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: Item):
    await item.save()
    if not item:
        raise HTTPException(status_code=404, detail="Couldn't create item.")
    return item


@router.get("/{id}/", response_model=Item)
async def read_item(
    id: int = Path(..., gt=0),
):
    item = await Item.objects.get(pk=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    return item


@router.get("/", response_model=List[Item])
async def read_all_items():
    return await Item.objects.select_related("categories").all()


@router.put("/{id}/", response_model=Item)
async def update_item(item_id: int, item: Item):
    item_db = await Item.objects.get(pk=item_id)
    if not item_db:
        raise HTTPException(status_code=404, detail="Item not found.")
    return await item_db.update(**item.dict())


@router.delete("/{id}/", response_model=Item)
async def delete_item(id: int, item: Item = None):
    if item:
        return {"deleted_rows": await item.delete()}

    item_db = await Item.objects.get(pk=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")

    return {"deleted_rows": await item_db.delete()}
