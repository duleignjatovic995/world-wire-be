import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), ".."))

from src.settings import settings  # noqa
from src.common.models import *  # isort:skip  # noqa


config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name, disable_existing_loggers=False)


target_metadata = Base.metadata  # noqa


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_connection_options(
    configuration, env_prefix="SQL_ALCHEMY_", ini_prefix="sqlalchemy."
):
    """
    Prioritize environment variables over `alembic.ini` hardcoded values for sqlalchemy
    configuration.

    First make options dict from config.ini vars, then merge them with env vars, thus
    giving env vars the priority.

    Usage example (with default params):
    alembic.ini
    >>>
        [alembic]
        ...
        sqlalchemy.demo_var = 0

    environment
    >>>
        export SQL_ALCHEMY_DEMO_VAR = 1

    returns:
    >>> {'demo_var': 1, '_coerce_config': True}

    :param configuration: basically any dict, but preferably an alembic config file's
        ini section - retrieve with config.get_section(config.config_ini_section)
    :param env_prefix: env var prefix
    :param ini_prefix: alembic.ini file config section prefix
    :return: config dict
    """
    options = dict(
        (key[len(ini_prefix) :], configuration[key])  # noqa E203
        for key in configuration
        if key.startswith(ini_prefix)
    )

    options.update(
        dict(
            (key[len(env_prefix) :].lower(), os.environ.get(key))  # noqa E203
            for key in os.environ
            if key.startswith(env_prefix)
        )
    )

    try:
        del options["url"]  # we are setting the url through separate function
    except KeyError:
        ...
    options["_coerce_config"] = True
    return options


def _get_connection_url():
    """
    Make use of environment variables instead of
    hardcoded values in `alembic.ini` file.
    :return: sqlalchemy connection string
    """
    return settings.DB_CONNECTION


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = _get_connection_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    connectable = create_engine(
        _get_connection_url(), **get_connection_options(configuration)
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
