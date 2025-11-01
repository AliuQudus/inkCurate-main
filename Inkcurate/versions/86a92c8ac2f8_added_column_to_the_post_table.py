"""Added column to the post table

Revision ID: 86a92c8ac2f8
Revises: 923956971ec3
Create Date: 2025-11-01 06:47:02.566109

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = "86a92c8ac2f8"
down_revision: Union[str, Sequence[str], None] = "923956971ec3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("email", sa.String(), nullable=False, unique=True))
    op.add_column("users", sa.Column("password", sa.String(), nullable=False))
    op.add_column(
        "users",
        sa.Column(
            "created at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
        ),
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "email")
    op.drop_column("users", "password")
    op.drop_column("users", "created at")
    pass
