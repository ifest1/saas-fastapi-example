from fastapi import APIRouter, FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.core.utils import initial_migration

from app.api.api_v1.api import api_router
from app.core.config import settings
import app.db.base as base
from app.middlewares.session import AnonymousUserMiddleware

from fastapi.middleware.cors import CORSMiddleware


root_router = APIRouter()
app = FastAPI(title="Ecommerce backend")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AnonymousUserMiddleware)
app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)


@app.on_event("startup")
async def startup():
    initial_migration()
    if not base.database.is_connected:
        await base.database.connect()


@app.on_event("shutdown")
async def shutdown():
    if not base.database.is_connected:
        await base.database.disconnect()


app.include_router(api_router, prefix=settings.API_VERSION)
app.include_router(root_router)
