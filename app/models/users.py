import ormar
from pydantic import EmailStr

from app.core.models import AppBaseModel
from app.db.base import BaseMeta


class User(ormar.Model, AppBaseModel):
    class Meta(BaseMeta):
        tablename = "users"

    first_name: str = ormar.String(max_length=256, nullable=True)
    surname: str = ormar.String(max_length=256, nullable=True)
    email: EmailStr = ormar.String(max_length=128, unique=True, nullable=False)
    is_active: bool = ormar.Boolean(default=True, nullable=False)
    is_superuser: bool = ormar.Boolean(default=False)
    hashed_password: str = ormar.String(max_length=256, nullable=False)
