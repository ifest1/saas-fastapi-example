import databases
import ormar
import sqlalchemy
from app.core.config import settings


database = databases.Database(settings.DB_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(settings.DB_URL)


if not sqlalchemy.inspect(engine).has_table("tenants"):
    tenants = sqlalchemy.Table(
        "tenants",
        metadata,
        sqlalchemy.Column("name", sqlalchemy.String),
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        schema="public",
    )

engine.dispose()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
