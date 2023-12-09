"""adding game_played column

Revision ID: 529e4afbcf18
Revises: 3751ac2dc3b6
Create Date: 2023-09-07 14:17:18.605761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '529e4afbcf18'
down_revision: Union[str, None] = '3751ac2dc3b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Player_stats', sa.Column('game_played', sa.INT))


def downgrade() -> None:
    pass
