from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7b4e1dea38f6"
down_revision: Union[str, Sequence[str], None] = "38c1fc70e75d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Remove the integer sequence/serial default first.
    op.execute(
        """
        ALTER TABLE app.project
        ALTER COLUMN id DROP DEFAULT
        """
    )

    # Convert the column and generate a new UUID for every existing row.
    op.alter_column(
        "project",
        "id",
        existing_type=sa.Integer(),
        type_=sa.Uuid(),
        existing_nullable=False,
        postgresql_using="gen_random_uuid()",
        schema="app",
    )

    # Generate UUIDs automatically for future rows.
    op.execute(
        """
        ALTER TABLE app.project
        ALTER COLUMN id SET DEFAULT gen_random_uuid()
        """
    )


def downgrade() -> None:
    raise RuntimeError(
        "This migration cannot restore the original integer IDs."
    )