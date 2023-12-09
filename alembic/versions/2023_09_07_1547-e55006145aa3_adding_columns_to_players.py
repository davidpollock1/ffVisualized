"""adding columns to Players

Revision ID: e55006145aa3
Revises: 0dd6cfdf9dc8
Create Date: 2023-09-07 15:47:20.361491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e55006145aa3'
down_revision: Union[str, None] = '0dd6cfdf9dc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Players', sa.Column('eligible_slots', sa.String)),
    op.add_column('Players', sa.Column('acquisition_type', sa.String)),
    op.add_column('Players', sa.Column('pro_team', sa.String)),
    op.add_column('Players', sa.Column('percent_owned', sa.INT)),
    op.add_column('Players', sa.Column('percent_started', sa.INT))

def downgrade() -> None:
    pass
