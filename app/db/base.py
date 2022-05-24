import databases
import ormar
import sqlalchemy

from ..core.config import settings

database = databases.Database(settings.DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


engine = sqlalchemy.create_engine(settings.DB_URL)
metadata.create_all(engine)
