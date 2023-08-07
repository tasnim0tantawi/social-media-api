"""create posts table

Revision ID: d41d5837c919
Revises: 30123b4bdcd2
Create Date: 2023-08-07 20:27:07.795642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd41d5837c919'
down_revision: Union[str, None] = '30123b4bdcd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('visibility', sa.String(10), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('posts')

