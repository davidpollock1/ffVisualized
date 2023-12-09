"""empty message

Revision ID: 14e3ecdba4bb
Revises: 4424e2d0de4b
Create Date: 2023-09-07 14:11:55.010699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14e3ecdba4bb'
down_revision: Union[str, None] = '4424e2d0de4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
