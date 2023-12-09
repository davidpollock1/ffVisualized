"""adding columns to Player_stats

Revision ID: 0dd6cfdf9dc8
Revises: 529e4afbcf18
Create Date: 2023-09-07 14:27:36.504034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0dd6cfdf9dc8'
down_revision: Union[str, None] = '529e4afbcf18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Player_stats', sa.Column('game_date', sa.DateTime)),
    op.add_column('Player_stats', sa.Column('on_bye_week', sa.Boolean)),
    op.add_column('Player_stats', sa.Column('pro_opponent', sa.String)),
    op.add_column('Player_stats', sa.Column('pro_pos_rank', sa.INT))


def downgrade() -> None:
    pass
