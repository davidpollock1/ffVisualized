"""empty message

Revision ID: 3751ac2dc3b6
Revises: 14e3ecdba4bb
Create Date: 2023-09-07 14:16:33.830215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3751ac2dc3b6'
down_revision: Union[str, None] = '14e3ecdba4bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
