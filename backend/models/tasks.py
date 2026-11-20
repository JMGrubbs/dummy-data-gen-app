from uuid import UUID
from typing import Any

from db.base import Base
from sqlalchemy import Index, Integer, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class DataGenTask(Base):
    __tablename__ = "task"

    __table_args__ = (
        Index("ix_task_user_id", "user_id"),
        {"schema": "app"},
    )

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    url_destination: Mapped[str] = mapped_column(nullable=False)

    data_bp: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    remaining_requests: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    requests_per_min: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        nullable=False,
        default="pending",
    )
