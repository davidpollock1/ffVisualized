"""remove position column from player_stats

Revision ID: 3dbef0cad1bd
Revises: e55006145aa3
Create Date: 2023-09-09 15:10:26.267209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dbef0cad1bd'
down_revision: Union[str, None] = 'e55006145aa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('Player_stats') as batch_op:
        batch_op.drop_column('position')


def downgrade() -> None:
    pass
