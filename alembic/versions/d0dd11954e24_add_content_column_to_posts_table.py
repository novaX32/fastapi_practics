"""add content column to posts table

Revision ID: d0dd11954e24
Revises: 472dba3a6782
Create Date: 2025-08-31 14:28:24.263855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0dd11954e24'
down_revision: Union[str, Sequence[str], None] = '472dba3a6782'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
