from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData(schema="app")


class Base(DeclarativeBase):
    metadata = metadata


from models import (
    tasks,  # noqa: F401 # Registers table with Alembic metadata.
    login_log,  # noqa: F401  # Registers table with Alembic metadata.
    project,  # noqa: F401  # Registers table with Alembic metadata.
)
