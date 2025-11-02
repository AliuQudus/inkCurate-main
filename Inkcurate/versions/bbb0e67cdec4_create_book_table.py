"""create book table

Revision ID: bbb0e67cdec4
Revises: 86a92c8ac2f8
Create Date: 2025-11-02 05:16:30.986434

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = "bbb0e67cdec4"
down_revision: Union[str, Sequence[str], None] = "86a92c8ac2f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "books",
        sa.Column(
            "id", sa.Integer(), primary_key=True, nullable=False, autoincrement=True
        ),
        sa.Column("book_id", sa.Integer(), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("authors", sa.JSON(), nullable=True),
        sa.Column("thumbnail", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "created at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
            onupdate=text("now()"),
        ),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    sa.drop_table("books")
    pass
