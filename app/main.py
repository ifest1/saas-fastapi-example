from fastapi import APIRouter, FastAPI

import app.db.base as base
from app.api.api_v1.api import api_router
from app.core.config import settings

root_router = APIRouter()
app = FastAPI(title="FastAPI, Docker, and Traefik Ecommerce.")


@app.on_event("startup")
async def startup():
    if not base.database.is_connected:
        await base.database.connect()


@app.on_event("shutdown")
async def shutdown():
    if not base.database.is_connected:
        await base.database.disconnect()


app.include_router(api_router, prefix=settings.API_VERSION)
app.include_router(root_router)
