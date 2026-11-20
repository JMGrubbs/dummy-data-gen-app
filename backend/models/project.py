import uuid
from datetime import datetime

from db.base import Base
from sqlalchemy import DateTime, Index, Integer, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column


class Project(Base):
    __tablename__ = "project"

    __table_args__ = (
        Index("ix_project_user_id", "user_id"),
        {"schema": "app"},
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )