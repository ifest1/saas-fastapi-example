from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, carts, categories, items, tenants

api_router = APIRouter()
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(
    categories.router, prefix="/categories", tags=["categories"]
)
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(carts.router, prefix="/carts", tags=["carts"])
