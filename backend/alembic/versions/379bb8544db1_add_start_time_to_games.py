"""add_start_time_to_games

Revision ID: 379bb8544db1
Revises: c943fd8f64a7
Create Date: 2026-04-09 10:43:03.312522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '379bb8544db1'
down_revision: Union[str, Sequence[str], None] = 'c943fd8f64a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE games ADD COLUMN start_time TIMESTAMPTZ")


def downgrade() -> None:
    op.execute("ALTER TABLE games DROP COLUMN start_time")
