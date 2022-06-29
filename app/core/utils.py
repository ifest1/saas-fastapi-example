import argparse
from alembic.config import Config
from alembic import command
from app.core.config import settings


def _get_alembic_cfg():
    alembic_cfg = Config(settings.ALEMBIC_CONF_FILE)
    alembic_cfg.cmd_opts = argparse.Namespace()
    setattr(alembic_cfg.cmd_opts, "x", [])
    alembic_cfg.set_main_option(
        "script_location", settings.ALEMBIC_SCRIPT_LOCATION
    )
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DB_URL)
    return alembic_cfg


def initial_migration():
    alembic_cfg = _get_alembic_cfg()
    alembic_cfg.cmd_opts.x = [
        "tenant=tenant_default",
    ]
    command.revision(
        alembic_cfg,
        "Create tables",
        True,
    )
    command.upgrade(alembic_cfg, "head")


def create_tenant_migration(tenant_name: str) -> None:
    alembic_cfg = _get_alembic_cfg()
    alembic_cfg.cmd_opts.x = ["tenant=,".format(tenant_name)]
    command.upgrade(alembic_cfg, "head")
