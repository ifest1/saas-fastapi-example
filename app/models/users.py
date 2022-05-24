import ormar
from pydantic import BaseModel

from app.db.base import BaseMeta


# Validation models
class UserSignIn(BaseModel):
    email: str
    password: str


class UserSignUp(BaseModel):
    first_name: str
    surname: str
    email: str
    password: str


# Models + ORM
class UserBase:
    id: int = ormar.Integer(primary_key=True)
    first_name: str = ormar.String(max_length=256, nullable=True)
    surname: str = ormar.String(max_length=256, nullable=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    is_active: bool = ormar.Boolean(default=True, nullable=False)
    is_superuser: bool = ormar.Boolean(default=False)


class User(ormar.Model, UserBase):
    class Meta(BaseMeta):
        tablename = "users"

    hashed_password: str = ormar.String(max_length=256, nullable=False)
