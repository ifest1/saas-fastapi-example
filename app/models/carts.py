import ormar

from app.db.base import BaseMeta


class Cart(ormar.Model):
    class Meta(BaseMeta):
        tablename = "carts"

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)
