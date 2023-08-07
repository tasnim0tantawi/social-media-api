"""create reactions table

Revision ID: 2997bf77f3d4
Revises: d41d5837c919
Create Date: 2023-08-07 21:07:38.212734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2997bf77f3d4'
down_revision: Union[str, None] = 'd41d5837c919'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'reactions',
        sa.Column('reaction_type', sa.String(50), nullable=False, server_default='like'),
        sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=sa.func.now(), nullable=False)
    )
        


def downgrade() -> None:
    op.drop_table('reactions')
