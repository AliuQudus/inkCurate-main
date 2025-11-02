"""Create likes table

Revision ID: 6bc7edfa1258
Revises: bbb0e67cdec4
Create Date: 2025-11-02 06:31:17.901490

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = "6bc7edfa1258"
down_revision: Union[str, Sequence[str], None] = "bbb0e67cdec4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "likes",
        sa.Column(
            "id", sa.Integer(), primary_key=True, nullable=False, autoincrement=True
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "book_id",
            sa.Integer(),
            sa.ForeignKey("books.id", ondelete="CASCADE"),
            nullable=False,
        ),
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
    op.drop_table("likes")
    pass
