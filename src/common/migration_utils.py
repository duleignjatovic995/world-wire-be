import os

from alembic.command import upgrade
from alembic.config import Config

from src.settings import settings


def execute_migrations():
    migrations_dir = os.path.join(settings.BASE_DIR, "migrations")
    config_file = os.path.join(settings.BASE_DIR, "alembic.ini")

    config = Config(file_=config_file)
    config.set_main_option("script_location", migrations_dir)

    # upgrade the database to the latest revision
    upgrade(config, "head")
