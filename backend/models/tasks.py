from typing import Any, TYPE_CHECKING
from uuid import UUID

from db.base import Base
from sqlalchemy import ForeignKey, Index, Integer, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.project import Project


class Task(Base):
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
        Uuid(as_uuid=True),
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

    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "app.project.id",
            name="fk_task_project_id_project",
        ),
        nullable=False,
        index=True,
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="tasks",
    )