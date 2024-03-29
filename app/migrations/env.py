import sys

sys.path = ["", ".."] + sys.path[1:]
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool, event
from sqlalchemy.schema import CreateSchema
from sqlalchemy import exc
from app.db.base import BaseMeta
from app.models.items import Category, Item
from app.models.users import User
from app.models.orders import Payment
from app.models.orders import Order

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = BaseMeta.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    def process_revision_directives(context, revision, directives):
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            print("No changes in schema detected.")

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    current_tenant = context.get_x_argument(as_dictionary=True).get("tenant")

    try:
        if current_tenant is not None:
            connectable.execute(CreateSchema(current_tenant))
    except Exception:
        pass

    with connectable.connect() as connection:
        connection.execute("set search_path to %s" % current_tenant)
        connection.dialect.default_schema_name = current_tenant
        schema_translate_map = {None: current_tenant}
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            schema_translate_map=schema_translate_map,
            version_table_schema="public",
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
