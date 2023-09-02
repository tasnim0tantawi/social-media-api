"""validate

Revision ID: a2575f4a5091
Revises: 2997bf77f3d4
Create Date: 2023-08-07 21:16:06.579900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a2575f4a5091'
down_revision: Union[str, None] = '2997bf77f3d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=True))
    op.alter_column('posts', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    op.alter_column('reactions', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('reactions', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    op.alter_column('posts', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    op.drop_column('posts', 'published')
    # ### end Alembic commands ###